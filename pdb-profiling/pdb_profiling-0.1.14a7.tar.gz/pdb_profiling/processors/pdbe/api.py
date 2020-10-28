# @Created Date: 2020-01-12 01:27:18 pm
# @Filename: api.py
# @Email:  1730416009@stu.suda.edu.cn
# @Author: ZeFeng Zhu
# @Last Modified: 2020-02-11 04:22:22 pm
# @Copyright (c) 2020 MinghuiGroup, Soochow University
import os
import numpy as np
import pandas as pd
from tablib import Dataset, InvalidDimensions, UnsupportedFormat
from typing import Union, Optional, Iterator, Iterable, Set, Dict, List, Any, Generator, Callable, Tuple
from json import JSONDecodeError
import orjson as json
from pathlib import Path
from aiofiles import open as aiofiles_open
from collections import defaultdict
from unsync import unsync, Unfuture
from pdb_profiling import default_id_tag
from pdb_profiling.utils import decompression, related_dataframe, flatten_dict, pipe_out, SeqRangeReader, sort_2_range
from pdb_profiling.log import Abclog
from pdb_profiling.fetcher.webfetch import UnsyncFetch
from pdb_profiling.processors.transformer import Dict2Tabular
from pdb_profiling.exceptions import WithoutExpectedKeyError

API_LYST: List = sorted(['summary', 'molecules', 'experiment', 'ligand_monomers',
                   'modified_AA_or_NA', 'mutated_AA_or_NA', 'status',
                   'polymer_coverage', 'secondary_structure',
                   'residue_listing', 'binding_sites', 'files', 'observed_residues_ratio',
                   'assembly', 'electron_density_statistics',
                   'cofactor', 'drugbank', 'related_experiment_data'])

BASE_URL: str = 'https://www.ebi.ac.uk/pdbe/'

FTP_URL: str = 'ftp://ftp.ebi.ac.uk/'

FTP_DEFAULT_PATH: str = 'pub/databases/msd/sifts/flatfiles/tsv/uniprot_pdb.tsv.gz'

PDB_ARCHIVE_URL_EBI: str = 'http://ftp.ebi.ac.uk/pub/databases/pdb/data/structures/'
PDB_ARCHIVE_URL_WWPDB: str = 'https://ftp.wwpdb.org/pub/pdb/data/structures/'
PDB_ARCHIVE_VERSIONED_URL: str = 'http://ftp-versioned.wwpdb.org/pdb_versioned/data/'

# https://ftp.wwpdb.org/pub/pdb/data/structures/obsolete/mmCIF/a0/2a01.cif.gz
# http://ftp.ebi.ac.uk/pub/databases/pdb/data/structures/obsolete/mmCIF/a0/2a01.cif.gz
# http://ftp-versioned.wwpdb.org/pdb_versioned/data/entries/wm/pdb_00002wmg/pdb_00002wmg_xyz_v1-2.cif.gz

FUNCS = list()


def str_number_converter(x):
    try:
        return int(x)
    except ValueError:
        return -1


def dispatch_on_set(keys: Set):
    '''
    Decorator to add new dispatch functions
    '''
    def register(func):
        FUNCS.append((func, frozenset(keys)))
        return func
    return register


def traverseSuffixes(query: Any, *args):
    for func, keySet in FUNCS:
        if query in keySet:
            return func(*args)
    else:
        raise ValueError(f'Invalid query: {query}')


def convertJson2other(
        data: Union[List, str, None], 
        append_data: Union[Iterable, Iterator],
        converter: Optional[Dataset] = None, 
        export_format: str = 'tsv', 
        ignore_headers: Union[bool, int] = False, 
        log_func=print) -> Any:
    '''
    Convert valid json-string/dict into specified format via `tablib.Dataset.export`
    '''
    if converter is None:
        converter = Dataset()
    try:
        if isinstance(data, str):
            converter.json = data
        elif isinstance(data, List):
            converter.dict = data
        elif data is None:
            pass
        else:
            log_func(f'Invalid type for data`: {type(data)}')
            return None
        for data_to_append in append_data:
            converter.append_col(*data_to_append)
        if ignore_headers:
            converter.headers = None
        return converter.export(export_format)
    except KeyError:
        log_func('Not a valid json-string/dict to convert format via `tablib.Dataset.export`')
    except JSONDecodeError:
        log_func(f'Invalid json string')
    except InvalidDimensions:
        log_func('Invalid data or append_data')
    except UnsupportedFormat:
        log_func(f'Invalid export_format: {export_format}')


class ProcessPDBe(Abclog):

    converters = {
        'pdb_id': str,
        'chain_id': str,
        'struct_asym_id': str,
        'entity_id': str_number_converter,
        'author_residue_number': int,
        'residue_number': str_number_converter,
        'author_insertion_code': str,
        'id': int,
        'interface_id': int,
        'interface_number': int,
        'pdb_code': str,
        'assemble_code': int,
        'assembly_id': int,
        'oper_expression': str,
        'structure_1.range': str,
        'structure_2.range': str
        }
    
    use_existing: bool = False

    @staticmethod
    def yieldTasks(pdbs: Union[Iterable, Iterator], suffix: str, method: str, folder: str, chunksize: int = 25, task_id: int = 0) -> Generator:
        file_prefix = suffix.replace('/', '%')
        method = method.lower()
        if method == 'post':
            url = f'{BASE_URL}{suffix}'
            for i in range(0, len(pdbs), chunksize):
                params = {'url': url, 'data': ','.join(pdbs[i:i+chunksize])}
                yield method, params, os.path.join(folder, f'{file_prefix}+{task_id}+{i}.json')
        elif method == 'get':
            for pdb in pdbs:
                # pdb = pdb.lower()
                identifier = pdb.replace('/', '%')
                yield method, {'url': f'{BASE_URL}{suffix}{pdb}'}, os.path.join(folder, f'{file_prefix}+{identifier}.json')
        else:
            raise ValueError(f'Invalid method: {method}, method should either be "get" or "post"')

    @classmethod
    def single_retrieve(cls, pdb: str, suffix: str, method: str, folder: Union[Path, str], semaphore, rate: float = 1.5, **kwargs):
        return UnsyncFetch.single_task(
            task=next(cls.yieldTasks((pdb, ), suffix, method, folder)),
            semaphore=semaphore,
            to_do_func=kwargs.get('to_do_func', cls.process),
            rate=rate)

    @classmethod
    def retrieve(cls, pdbs: Union[Iterable, Iterator], suffix: str, method: str, folder: str, chunksize: int = 20, concur_req: int = 20, rate: float = 1.5, task_id: int = 0, ret_res:bool=True, **kwargs):
        # t0 = time.perf_counter()
        res = UnsyncFetch.multi_tasks(
            cls.yieldTasks(pdbs, suffix, method, folder, chunksize, task_id), 
            cls.process, 
            concur_req=concur_req, 
            rate=rate, 
            ret_res=ret_res,
            semaphore=kwargs.get('semaphore', None))
        # elapsed = time.perf_counter() - t0
        # cls.logger.info('{} ids downloaded in {:.2f}s'.format(len(res), elapsed))
        return res
    
    @classmethod
    @unsync
    async def process(cls, path: Union[str, Path, Unfuture]):
        cls.logger.debug('Start to decode')
        if not isinstance(path, (str, Path)):
            path = await path # .result()
        if path is None:
            return path
        path = Path(path)
        suffix = path.name.replace('%', '/').split('+')[0]
        new_path = Path(str(path).replace('.json', '.tsv'))
        if new_path.exists() and cls.use_existing and (new_path.stat().st_size > 0):
            return new_path
        async with aiofiles_open(path) as inFile:
            try:
                data = json.loads(await inFile.read())
            except Exception as e:
                cls.logger.error(f"Error in {path}")
                raise e
        if new_path.exists() and cls.use_existing and (new_path.stat().st_size > 0):
            return new_path
        res = Dict2Tabular.pyexcel_io(traverseSuffixes(suffix, data))
        if res is not None:
            if isinstance(res, Generator):
                count = 0
                for r in res:
                    if r is not None:
                        await pipe_out(df=r, path=new_path, format='tsv', mode='a' if count else 'w')
                        count += 1
                if not count:
                    cls.logger.debug(f"Without Expected Data ({suffix}): {data}")
                    return None
            else:
                await pipe_out(df=res, path=new_path, format='tsv', mode='w')
            cls.logger.debug(f'Decoded file in {new_path}')
            return new_path
        else:
            cls.logger.debug(f"Without Expected Data ({suffix}): {data}")
            return None
        

class ProcessSIFTS(ProcessPDBe):
    @classmethod
    def related_UNP_PDB(cls, filePath: Union[str, Path], related_unp: Optional[Iterable] = None, related_pdb: Optional[Iterable] = None):
        '''
        Reference
        
            * http://www.ebi.ac.uk/pdbe/docs/sifts/quick.html
            * A summary of the UniProt to PDB mappings showing the UniProt accession
              followed by a semicolon-separated list of PDB four letter codes.
        '''
        filePath = Path(filePath)
        if filePath.is_dir():
            url = FTP_URL+FTP_DEFAULT_PATH
            task = ('ftp', {'url': url}, str(filePath))
            res = UnsyncFetch.multi_tasks([task]).result()
            filePath = decompression(res[0], remove=False, logger=cls.logger)
        elif filePath.is_file() and filePath.exists():
            filePath = str(filePath)
        else:
            raise ValueError('Invalid value for filePath')

        dfrm = pd.read_csv(filePath, sep='\t', header=1)
        pdb_list = list()
        if related_unp is not None:
            dfrm = dfrm[dfrm['SP_PRIMARY'].isin(related_unp)]
        for i in dfrm.index:
            pdb_list.extend(dfrm.loc[i, 'PDB'].split(';'))
        if related_pdb is not None:
            return set(pdb_list) & set(related_pdb), set(dfrm['SP_PRIMARY'])
        else:
            return set(pdb_list), set(dfrm['SP_PRIMARY'])

    @classmethod
    def reformat(cls, path: Optional[str]=None, dfrm:Optional[pd.DataFrame]=None) -> pd.DataFrame:
        if path is not None:
            dfrm = pd.read_csv(path, sep='\t', converters=cls.converters)
        group_info_col = ['pdb_id', 'chain_id', 'UniProt']
        range_info_col = ['pdb_start', 'pdb_end', 'unp_start', 'unp_end']
        reader = SeqRangeReader(group_info_col)
        dfrm[['pdb_range', 'unp_range']] = pd.DataFrame(dfrm.apply(
            lambda x: reader.check(tuple(x[i] for i in group_info_col), tuple(
                x[i] for i in range_info_col)),
            axis=1).values.tolist(), index=dfrm.index)
        dfrm = dfrm.drop(columns=range_info_col).drop_duplicates(
            subset=group_info_col, keep='last').reset_index(drop=True)
        dfrm["Entry"] = dfrm["UniProt"].apply(lambda x: x.split('-')[0])
        return dfrm

    @classmethod
    def dealWithInDel(cls, dfrm: pd.DataFrame, sort_by_unp:bool=True) -> pd.DataFrame:
        def get_gap_list(li: List):
            return [li[i+1][0] - li[i][1] - 1 for i in range(len(li)-1)]

        def get_range_diff(lyst_a: List, lyst_b: List):
            array_a = np.array([right - left + 1 for left, right in lyst_a])
            array_b = np.array([right - left + 1 for left, right in lyst_b])
            return array_a - array_b

        def add_tage_to_range(df: pd.DataFrame, tage_name: str):
            # ADD TAGE FOR SIFTS
            df[tage_name] = 'Safe'
            # No Insertion But Deletion[Pure Deletion]
            df.loc[df[(df['group_info'] == 1) & (
                df['diff+'] > 0)].index, tage_name] = 'Deletion'
            # Insertion & No Deletion
            df.loc[df[
                (df['group_info'] == 1) &
                (df['diff-'] > 0)].index, tage_name] = 'Insertion_Undivided'
            df.loc[df[
                (df['group_info'] > 1) &
                (df['diff0'] == df['group_info']) &
                (df['unp_gaps0'] == (df['group_info'] - 1))].index, tage_name] = 'Insertion'
            # Insertion & Deletion
            df.loc[df[
                (df['group_info'] > 1) &
                (df['diff0'] == df['group_info']) &
                (df['unp_gaps0'] != (df['group_info'] - 1))].index, tage_name] = 'InDel_1'
            df.loc[df[
                (df['group_info'] > 1) &
                (df['diff0'] != df['group_info']) &
                (df['unp_gaps0'] != (df['group_info'] - 1))].index, tage_name] = 'InDel_2'
            df.loc[df[
                (df['group_info'] > 1) &
                (df['diff0'] != df['group_info']) &
                (df['unp_gaps0'] == (df['group_info'] - 1))].index, tage_name] = 'InDel_3'

        dfrm.pdb_range = dfrm.pdb_range.apply(json.loads)
        dfrm.unp_range = dfrm.unp_range.apply(json.loads)
        dfrm['group_info'] = dfrm.apply(lambda x: len(
            x['pdb_range']), axis=1)

        focus_index = dfrm[dfrm.group_info.gt(1)].index
        if sort_by_unp and (len(focus_index) > 0):
            focus_df = dfrm.loc[focus_index].apply(lambda x: sort_2_range(
                x['unp_range'], x['pdb_range']), axis=1, result_type='expand')
            focus_df.index = focus_index
            focus_df.columns = ['unp_range', 'pdb_range']
            dfrm.loc[focus_index, ['unp_range', 'pdb_range']] = focus_df

        dfrm['pdb_gaps'] = dfrm.pdb_range.apply(get_gap_list)
        dfrm['unp_gaps'] = dfrm.unp_range.apply(get_gap_list)
        dfrm['range_diff'] = dfrm.apply(lambda x: get_range_diff(x['unp_range'], x['pdb_range']), axis=1)
        dfrm['diff0'] = dfrm.range_diff.apply(lambda x: np.count_nonzero(x == 0))
        dfrm['diff+'] = dfrm.range_diff.apply(lambda x: np.count_nonzero(x > 0))
        dfrm['diff-'] = dfrm.range_diff.apply(lambda x: np.count_nonzero(x < 0))
        dfrm['unp_gaps0'] = dfrm.unp_gaps.apply(lambda x: x.count(0))
        add_tage_to_range(dfrm, tage_name='sifts_range_tag')
        dfrm['repeated'] = dfrm.apply(
            lambda x: x['diff-'] > 0 and x['sifts_range_tag'] != 'Insertion_Undivided', axis=1)
        dfrm['repeated'] = dfrm.apply(
            lambda x: True if any(i < 0 for i in x['unp_gaps']) else x['repeated'], axis=1)
        dfrm['reversed'] = dfrm.pdb_gaps.apply(lambda x: any(i < 0 for i in x))
        dfrm.pdb_range = dfrm.pdb_range.apply(lambda x: json.dumps(x).decode('utf-8'))
        dfrm.unp_range = dfrm.unp_range.apply(lambda x: json.dumps(x).decode('utf-8'))
        temp_cols = ['start', 'end', 'group_info', 'pdb_gaps', 'unp_gaps', 'range_diff',
                     'diff0', 'diff+', 'diff-', 'unp_gaps0']
        return dfrm.drop(columns=temp_cols), dfrm[temp_cols]
    
    '''
    @staticmethod
    def update_range(dfrm: pd.DataFrame, fasta_col: str, unp_fasta_files_folder: str, new_range_cols=('new_sifts_unp_range', 'new_sifts_pdb_range')) -> pd.DataFrame:
        def getSeq(fasta_path: str):
            unpSeq = None
            try:
                unpSeqOb = SeqIO.read(fasta_path, "fasta")
                unpSeq = unpSeqOb.seq
            except ValueError:
                unpSeqOb = SeqIO.parse(fasta_path, "fasta")
                for record in unpSeqOb:
                    if unp_id in record.id.split('|'):
                        unpSeq = record.seq
            return unpSeq

        focus = ('Deletion', 'Insertion & Deletion')
        focus_index = dfrm[dfrm['sifts_range_tage'].isin(focus)].index
        updated_pdb_range, updated_unp_range = list(), list()
        seqAligner = SeqPairwiseAlign()
        for index in focus_index:
            pdbSeq = dfrm.loc[index, fasta_col]
            unp_entry = dfrm.loc[index, "Entry"]
            unp_id = dfrm.loc[index, "UniProt"]
            try:
                fasta_path = os.path.join(
                    unp_fasta_files_folder, f'{unp_id}.fasta')
                unpSeq = getSeq(fasta_path)
            except FileNotFoundError:
                try:
                    fasta_path = os.path.join(
                        unp_fasta_files_folder, f'{unp_entry}.fasta')
                    unpSeq = getSeq(fasta_path)
                except FileNotFoundError:
                    unpSeq = None
            res = seqAligner.makeAlignment(unpSeq, pdbSeq)
            updated_unp_range.append(res[0])
            updated_pdb_range.append(res[1])

        updated_range_df = pd.DataFrame(
            {new_range_cols[0]: updated_unp_range, new_range_cols[1]: updated_pdb_range}, index=focus_index)
        dfrm = pd.merge(dfrm, updated_range_df, left_index=True,
                        right_index=True, how='left')
        dfrm[new_range_cols[0]] = dfrm.apply(lambda x: x['sifts_unp_range'] if pd.isna(
            x[new_range_cols[0]]) else x[new_range_cols[0]], axis=1)
        dfrm[new_range_cols[1]] = dfrm.apply(lambda x: x['sifts_pdb_range'] if pd.isna(
            x[new_range_cols[1]]) else x[new_range_cols[1]], axis=1)
        return dfrm

    @classmethod
    def main(cls, filePath: Union[str, Path], folder: str, related_unp: Optional[Iterable] = None, related_pdb: Optional[Iterable] = None):
        pdbs, _ = cls.related_UNP_PDB(filePath, related_unp, related_pdb)
        res = cls.retrieve(pdbs, 'mappings/all_isoforms/', 'get', folder)
        # return pd.concat((cls.dealWithInDe(cls.reformat(route)) for route in res if route is not None), sort=False, ignore_index=True)
        return res
    '''


class ProcessEntryData(ProcessPDBe):
    @staticmethod
    def related_PDB(pdb_col: str, **kwargs) -> pd.Series:
        dfrm = related_dataframe(**kwargs)
        return dfrm[pdb_col].drop_duplicates()

    @classmethod
    def main(cls, **kwargs):
        pdbs = cls.related_PDB(**kwargs)
        if len(pdbs) > 0:
            res = cls.retrieve(pdbs, **kwargs)
            try:
                return pd.concat((pd.read_csv(route, sep=kwargs.get('sep', '\t'), converters=cls.converters) for route in res if route is not None), sort=False, ignore_index=True)
            except ValueError:
                cls.logger.error('Non-value to concat')
        else:
            return None

    @classmethod
    def unit(cls, pdbs, **kwargs):
        if len(pdbs) > 0:
            res = cls.retrieve(pdbs, **kwargs)
            try:
                return pd.concat((pd.read_csv(route, sep=kwargs.get('sep', '\t'), converters=cls.converters) for route in res if route is not None), sort=False, ignore_index=True)
            except ValueError:
                cls.logger.warning('Non-value to concat')
        else:
            return None

    @staticmethod
    def yieldObserved(dfrm: pd.DataFrame) -> Generator:
        groups = dfrm.groupby(['pdb_id', 'entity_id', 'chain_id'])
        for i, j in groups:
            mod = j.dropna(subset=['chem_comp_id'])
            yield i, len(j[j.observed_ratio.gt(0)]), len(mod[mod.observed_ratio.gt(0)])

    @staticmethod
    def traverse(data: Dict, cols: Tuple, cutoff=50):
        '''
        temp
        '''
        observed_res_count, observed_modified_res_count = cols
        for pdb in data:
            count = 0
            cleaned = 0
            for entity in data[pdb].values():
                for chain in entity.values():
                    if chain[observed_res_count] - chain[observed_modified_res_count] < cutoff:
                        cleaned += 1
                    count += 1
            yield pdb, count, cleaned

    @classmethod
    def pipeline(cls, pdbs: Iterable, folder: str, chunksize: int = 1000):
        for i in range(0, len(pdbs), chunksize):
            related_pdbs = pdbs[i:i+chunksize]
            molecules_dfrm = ProcessEntryData.unit(
                related_pdbs,
                suffix='api/pdb/entry/molecules/',
                method='post',
                folder=folder,
                task_id=i)
            res_listing_dfrm = ProcessEntryData.unit(
                related_pdbs,
                suffix='api/pdb/entry/residue_listing/',
                method='get',
                folder=folder,
                task_id=i)
            modified_AA_dfrm = ProcessEntryData.unit(
                related_pdbs,
                suffix='api/pdb/entry/modified_AA_or_NA/',
                method='post',
                folder=folder,
                task_id=i)
            if modified_AA_dfrm is not None:
                res_listing_dfrm.drop(columns=['author_insertion_code'], inplace=True)
                modified_AA_dfrm.drop(columns=['author_insertion_code'], inplace=True)
                res_listing_mod_dfrm = pd.merge(res_listing_dfrm, modified_AA_dfrm, how='left')
            else:
                res_listing_mod_dfrm = res_listing_dfrm
                res_listing_mod_dfrm['chem_comp_id'] = np.nan
            pro_dfrm = molecules_dfrm[molecules_dfrm.molecule_type.isin(['polypeptide(L)', 'polypeptide(D)'])][['pdb_id', 'entity_id']].reset_index(drop=True)
            pro_res_listing_mod_dfrm = pd.merge(res_listing_mod_dfrm, pro_dfrm)
            data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
            for (pdb_id, entity_id, chain_id), observed_res_count, observed_modified_res_count in cls.yieldObserved(pro_res_listing_mod_dfrm):
                data[pdb_id][entity_id][chain_id]['ob_res'] = observed_res_count
                data[pdb_id][entity_id][chain_id]['ob_moded_res'] = observed_modified_res_count
            with Path(folder, f'clean_pdb_statistic+{i}.tsv').open(mode='w+') as outFile:
                for tup in cls.traverse(data, ('ob_res', 'ob_moded_res')):
                    outFile.write('%s\t%s\t%s\n' % tup)
            with Path(folder, f'clean_pdb_statistic+{i}.json').open(mode='w+') as outFile:
                json.dump(data, outFile)


class PDBeDecoder(object):

    @staticmethod
    @dispatch_on_set({'api/pdb/entry/status/', 'api/pdb/entry/summary/', 'api/pdb/entry/modified_AA_or_NA/',
                      'api/pdb/entry/mutated_AA_or_NA/', 'api/pdb/entry/cofactor/', 'api/pdb/entry/molecules/',
                      'api/pdb/entry/ligand_monomers/', 'api/pdb/entry/experiment/', 'api/pdb/entry/carbohydrate_polymer/',
                      'api/pdb/entry/electron_density_statistics/', 'api/pdb/entry/related_experiment_data/',
                      'api/pdb/entry/drugbank/', 'api/mappings/best_structures/',
                      'graph-api/pdb/mutated_AA_or_NA/', 'graph-api/pdb/modified_AA_or_NA/',
                      'graph-api/mappings/best_structures/', 'graph-api/compound/atoms/',
                      'graph-api/compound/bonds/', 'graph-api/compound/summary/',
                      'graph-api/compound/cofactors/', 'graph-api/pdb/funpdbe/',
                      'graph-api/pdb/bound_excluding_branched/',
                      'graph-api/pdb/bound_molecules/', 'graph-api/pdb/ligand_monomers/'})
    def yieldCommon(data: Dict) -> Generator:
        for pdb in data:
            values = data[pdb]
            for value in values:
                for key in value:
                    if isinstance(value[key], (Dict, List)):
                        value[key] = json.dumps(value[key]).decode('utf-8')
            yield values, (default_id_tag(pdb, '_code_'),), (pdb,)

    @staticmethod
    @dispatch_on_set({'api/pdb/entry/polymer_coverage/'})
    def yieldPolymerCoverage(data: Dict) -> Generator:
        for pdb in data:
            molecules = data[pdb]['molecules']
            for entity in molecules:
                chains = entity['chains']
                for chain in chains:
                    observed = chain['observed']
                    for fragement in observed:
                        for key in ('start', 'end'):
                            fragement[key] = json.dumps(fragement[key]).decode('utf-8')
                    yield observed, ('chain_id', 'struct_asym_id', 'entity_id', 'pdb_id'), (chain['chain_id'], chain['struct_asym_id'], entity['entity_id'], pdb)

    @staticmethod
    @dispatch_on_set({'api/pdb/entry/observed_residues_ratio/'})
    def yieldObservedResiduesRatio(data: Dict) -> Generator:
        for pdb in data:
            for entity_id, entity in data[pdb].items():
                yield entity, ('entity_id', 'pdb_id'), (entity_id, pdb)

    @staticmethod
    @dispatch_on_set({'api/pdb/entry/residue_listing/'})
    def yieldResidues(data: Dict) -> Generator:
        for pdb in data:
            molecules = data[pdb]['molecules']
            for entity in molecules:
                chains = entity['chains']
                for chain in chains:
                    residues = chain['residues']
                    for res in residues:
                        if 'multiple_conformers' not in res:
                            res['multiple_conformers'] = ''
                        else:
                            res['multiple_conformers'] = json.dumps(res['multiple_conformers']).decode('utf-8')
                    yield residues, ('chain_id', 'struct_asym_id', 'entity_id', 'pdb_id'), (chain['chain_id'], chain['struct_asym_id'], entity['entity_id'], pdb)

    @staticmethod
    @dispatch_on_set({'api/pdb/entry/secondary_structure/', 'graph-api/pdb/secondary_structure/'})
    def yieldSecondaryStructure(data: Dict) -> Generator:
        for pdb in data:
            molecules = data[pdb]['molecules']
            for entity in molecules:
                chains = entity['chains']
                for chain in chains:
                    secondary_structure = chain['secondary_structure']
                    for name in secondary_structure:
                        fragment = secondary_structure[name]
                        for record in fragment:
                            for key in record:
                                if isinstance(record[key], (Dict, List)):
                                    record[key] = json.dumps(record[key]).decode('utf-8')
                            if 'sheet_id' not in record:
                                record['sheet_id'] = None
                        yield fragment, ('secondary_structure', 'chain_id', 'struct_asym_id', 'entity_id', 'pdb_id'), (name, chain['chain_id'], chain['struct_asym_id'], entity['entity_id'], pdb)

    @staticmethod
    @dispatch_on_set({'api/pdb/entry/binding_sites/'})
    def yieldBindingSites(data: Dict) -> Generator:
        for pdb in data:
            for site in data[pdb]:
                for tage in ('site_residues', 'ligand_residues'):
                    residues = site[tage]
                    for res in residues:
                        if 'symmetry_symbol' not in res:
                            res['symmetry_symbol'] = None
                    yield residues, ('residues_type', 'details', 'evidence_code', 'site_id', 'pdb_id'), (tage, site['details'], site['evidence_code'], site['site_id'], pdb)

    @staticmethod
    @dispatch_on_set({'api/pdb/entry/assembly/'})
    def yieldAssembly(data: Dict) -> Generator:
        for pdb in data:
            for biounit in data[pdb]:
                entities = biounit['entities']
                for entity in entities:
                    for key in entity:
                        if isinstance(entity[key], (Dict, List)):
                            entity[key] = json.dumps(entity[key]).decode('utf-8')
                keys = list(biounit)
                keys.remove('entities')
                yield entities, tuple(keys)+('pdb_id',), tuple(biounit[key] for key in keys)+(pdb, )

    @staticmethod
    @dispatch_on_set({'api/pdb/entry/files/'})
    def yieldAssociatedFiles(data: Dict) -> Generator:
        for pdb in data:
            for key in data[pdb]:
                for innerKey in data[pdb][key]:
                    record = data[pdb][key][innerKey]
                    if record:
                        yield record, ('innerKey', 'key', 'pdb_id'), (innerKey, key, pdb)
                    else:
                        continue

    @staticmethod
    @dispatch_on_set({'api/mappings/all_isoforms/', 'api/mappings/uniprot/',
                      'api/mappings/uniprot_segments/', 'api/mappings/isoforms/',
                      'api/mappings/uniref90/', 'api/mappings/homologene_uniref90/',
                      'api/mappings/interpro/', 'api/mappings/pfam/',
                      'api/mappings/cath/', 'api/mappings/cath_b/',
                      'api/mappings/scop/', 'api/mappings/go/',
                      'api/mappings/ec/', 'api/mappings/ensembl/',
                      'api/mappings/hmmer/', 'api/mappings/sequence_domains/',
                      'api/mappings/structural_domains/', 'api/mappings/homologene/',
                      'api/mappings/uniprot_to_pfam/', 'api/mappings/uniprot_publications/',
                      'graph-api/mappings/uniprot/', 'graph-api/mappings/uniprot_segments/',
                      'graph-api/mappings/all_isoforms/', 'graph-api/mappings/',
                      'graph-api/mappings/isoforms/', 'graph-api/mappings/ensembl/',
                      'graph-api/mappings/homologene/', 'graph-api/mappings/sequence_domains/'
                      # 'graph-api/uniprot/'
                      })
    def yieldSIFTSAnnotation(data: Dict) -> Generator:
        valid_annotation_set = {'UniProt', 'Ensembl', 'Pfam', 'CATH', 'CATH-B', 'SCOP', 'InterPro', 'GO', 'EC', 'Homologene', 'HMMER'}
        for top_root in data:
            # top_root: PDB_ID or else ID
            if data[top_root].keys() <= valid_annotation_set:
                # from PDB to ('UniProt', 'Ensembl', 'Pfam', 'CATH', 'CATH-B', 'SCOP', 'InterPro', 'GO', 'EC', 'Homologene', 'HMMER')
                # from PDB_ENTITY (i.e. graph-api/mappings/homologene/)
                # OR: from Uniprot (i.e. api/mappings/uniprot_to_pfam/)
                for sec_root in data[top_root]:
                    child = data[top_root][sec_root]
                    for annotation in child:
                        chains = child[annotation]['mappings']
                        for chain in chains:
                            for key, value in chain.items():
                                chain[key] = json.dumps(value).decode('utf-8') if isinstance(value, Dict) else value
                            for key, value in child[annotation].items():
                                if key == 'mappings':
                                    continue
                                chain[key] = json.dumps(value).decode('utf-8') if isinstance(value, Dict) else value
                            chain[default_id_tag(top_root, raise_error=True)] = top_root
                            chain[sec_root] = annotation
                        yield chains, None
            elif len(data[top_root].keys()) == 1 and 'PDB' in data[top_root].keys():
                # from UniProt to PDB
                for sec_root in data[top_root]:
                    child = data[top_root][sec_root]
                    for pdb in child:
                        chains = child[pdb]
                        for chain in chains:
                            chain['start'] = json.dumps(chain['start']).decode('utf-8')
                            chain['end'] = json.dumps(chain['end']).decode('utf-8')
                        yield chains, ('pdb_id', 'UniProt'), (pdb, top_root)
            else:
                raise ValueError(f'Unexpected data structure for inputted data: {data}')

    @staticmethod
    @dispatch_on_set({'api/pisa/interfacelist/'})
    def yieldPISAInterfaceList(data: Dict):
        for pdb in data:
            try:
                records = data[pdb]['interfaceentries']
            except KeyError:
                raise WithoutExpectedKeyError(f"Without Expected interface_detail: {data}")
            for record in records:
                flatten_dict(record, 'structure_1')
                flatten_dict(record, 'structure_2')
            flatten_dict(data[pdb], 'page_title', False)
            cols = sorted(i for i in data[pdb].keys() if i != 'interfaceentries')
            yield records, cols, tuple(data[pdb][col] for col in cols)
    
    @staticmethod
    @dispatch_on_set({'api/pisa/interfacedetail/'})
    def yieldPISAInterfaceDetail(data: Dict):
        usecols = (
            'pdb_code', 'assemble_code', 'interface_number',
            'interface_detail.interface_structure_1.structure.selection',
            'interface_detail.interface_structure_2.structure.selection')
        edge_cols1 = ('structure',)  # 'interface_atoms', 'interface_residue', 'interface_area', 'solvation_energy'
        edge_cols2 = ('structure',)  # 'interface_atoms', 'interface_residues', 'interface_area', 'solvation_energy'
        for pdb in data:
            try:
                records = data[pdb]['interface_detail']
            except KeyError:
                raise WithoutExpectedKeyError(f"Without Expected interface_detail: {data}")
            del records['bonds']
            for col in edge_cols1: flatten_dict(records['interface_structure_1'], col)
            for col in edge_cols2: flatten_dict(records['interface_structure_2'], col)
            flatten_dict(data[pdb], 'page_title', False)
            flatten_dict(records, 'interface_structure_1')
            flatten_dict(records, 'interface_structure_2')
            flatten_dict(data[pdb], 'interface_detail')
            # cols = sorted(i for i in data[pdb].keys() if i != 'interface_detail.residues')
            yield data[pdb]['interface_detail.residues']['residue1']['residue']['residue_array'], usecols, tuple(data[pdb][col] for col in usecols)
            yield data[pdb]['interface_detail.residues']['residue2']['residue']['residue_array'], usecols, tuple(data[pdb][col] for col in usecols)

    @staticmethod
    @dispatch_on_set({'graph-api/residue_mapping/'})
    def graph_api_residue_mapping(data: Dict):
        '''
        * <https://www.ebi.ac.uk/pdbe/graph-api/residue_mapping/:pdbId/:entityId/:residueNumber>
        * <https://www.ebi.ac.uk/pdbe/graph-api/residue_mapping/:pdbId/:entityId/:residueStart/:residueEnd>

        NOTE: only yield UniProt Residue Related Data
        '''
        cols = (
            'pdb_id', 'entity_id', 'chain_id', 'struct_asym_id',
            'residue_number', 'author_residue_number',
            'author_insertion_code', 'observed', 'UniProt')

        for pdb_id in data:
            assert len(data[pdb_id]) == 1, f"Unexpected Cases: {pdb_id}"
            molecules = data[pdb_id][0]
            for chain in molecules['chains']:
                for residue in chain['residues']:
                    yield list({**dict(zip(cols, (
                        pdb_id, molecules['entity_id'], chain['auth_asym_id'],
                        chain['struct_asym_id'], residue['residue_number'],
                        residue['author_residue_number'], residue['author_insertion_code'],
                        residue['observed'], feature_tag))), **feature} for feature_tag, feature in residue['features']['UniProt'].items()), None


class PDBeModelServer(Abclog):
    '''
    Implement ModelServer API
    '''
    
    root = f'{BASE_URL}model-server/v1/'
    headers =  {'accept': 'text/plain', 'Content-Type': 'application/json'}
    api_set = frozenset(('atoms', 'residueInteraction', 'assembly', 'full', 'ligand'
                'residueSurroundings', 'symmetryMates', 'query-many'))
    
    @classmethod
    def yieldTasks(cls, pdbs, suffix: str, method: str, folder: str, data_collection, params) -> Generator:
        if data_collection is None:
            assert method == 'get', 'Invalid method!'
            for pdb in pdbs:
                args = dict(
                    url=f'{cls.root}{pdb}/{suffix}?',
                    headers=cls.headers,
                    params=params)
                yield method, args, os.path.join(folder, f'{pdb}_subset.{params.get("encoding", "cif")}')
        else:
            assert method == 'post', 'Invalid method!'
            for pdb, data in zip(pdbs, data_collection):
                args = dict(
                    url=f'{cls.root}{pdb}/{suffix}?',
                    headers=cls.headers,
                    params=params,
                    data=data)
                yield method, args, os.path.join(folder, f'{pdb}_subset.{params.get("encoding", "cif")}')

    @classmethod
    def retrieve(cls, pdbs, suffix: str, method: str, folder: str, data_collection=None, params=None, concur_req: int = 20, rate: float = 1.5, ret_res:bool=True, **kwargs):
        if params is None:
            params = {'model_nums': 1, 'encoding': 'cif'}
        res = UnsyncFetch.multi_tasks(
            cls.yieldTasks(pdbs, suffix, method, folder,
                           data_collection, params),
            concur_req=concur_req,
            rate=rate,
            ret_res=ret_res,
            semaphore=kwargs.get('semaphore', None))
        return res
    
    @classmethod
    def single_retrieve(cls, pdb: str, suffix: str, method: str, folder: Union[Path, str], semaphore, data_collection=None, params=None, rate: float = 1.5):
        if params is None:
            params = {'encoding': 'cif'}
        if data_collection is not None:
            data_collection = (data_collection, )
        return UnsyncFetch.single_task(
            task=next(cls.yieldTasks((pdb, ), suffix, method, folder,
                                     data_collection, params)),
            semaphore=semaphore,
            rate=rate)


class PDBArchive(Abclog):
    '''
    Download files from PDB Archive

    * wwPDB/RCSB: PDB_ARCHIVE_URL_WWPDB: str = 'https://ftp.wwpdb.org/pub/pdb/data/structures/'
    * EBI: PDB_ARCHIVE_URL_EBI: str = 'http://ftp.ebi.ac.uk/pub/databases/pdb/data/structures/'
    '''
    root = PDB_ARCHIVE_URL_EBI
    api_set = frozenset(f'{i}/{j}/' for i in ('obsolete', 'divided')
                for j in ('mmCIF', 'pdb', 'XML'))

    @classmethod
    def task_unit(cls, pdb: str, suffix: str, file_suffix: str, folder: Path):
        args = dict(url=f'{cls.root}{suffix}{pdb[1:3]}/{pdb}{file_suffix}')
        return 'get', args, folder/f'{pdb}{file_suffix}'

    @classmethod
    def yieldTasks(cls, pdbs, suffix: str, file_suffix: str, folder: Path) -> Generator:
        for pdb in pdbs:
            yield cls.task_unit(pdb, suffix, file_suffix, folder)

    @classmethod
    def retrieve(cls, pdbs, suffix: str, folder: Path, file_suffix: str = '.cif.gz', concur_req: int = 20, rate: float = 1.5, ret_res:bool=True, **kwargs):
        res = UnsyncFetch.multi_tasks(
            cls.yieldTasks(pdbs, suffix, file_suffix, folder),
            concur_req=concur_req,
            rate=rate,
            ret_res=ret_res,
            semaphore=kwargs.get('semaphore', None))
        return res
    
    @classmethod
    def single_retrieve(cls, pdb, suffix: str, folder: Path, semaphore, file_suffix: str = '.cif.gz', rate: float = 1.5):
        return UnsyncFetch.single_task(
            task=cls.task_unit(pdb, suffix, file_suffix, folder),
            semaphore=semaphore,
            rate=rate)


class PDBVersioned(PDBArchive):
    '''
    Download files from PDB Versioned

    * wwPDB Versioned: PDB_ARCHIVE_VERSIONED_URL: str = 'http://ftp-versioned.wwpdb.org/pdb_versioned/data/entries/'

    >>> PDBVersioned.single_retrieve(
        ('2wmg', '_v1-2'), 'entries/', 
        init_folder_from_suffix(Base.get_folder(), 'pdb-versioned/entries'), 
        Base.get_web_semaphore()).result()
    '''
    root = PDB_ARCHIVE_VERSIONED_URL
    api_set = frozenset(('entries/', 'removed/'))

    @classmethod
    def task_unit(cls, pdb_with_version: Tuple, suffix: str, file_suffix: str, folder: Path):
        pdb, version_info = pdb_with_version
        file_name = f'pdb_0000{pdb}_xyz{version_info}{file_suffix}'
        args = dict(url=f'{cls.root}{suffix}{pdb[1:3]}/pdb_0000{pdb}/{file_name}')
        return 'get', args, folder/file_name


# TODO: Chain UniProt ID Mapping -> ProcessSIFTS -> ProcessPDBe
# TODO: Deal with oligomeric PDB
