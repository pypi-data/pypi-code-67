#
# Copyright (c) nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from collections import OrderedDict
import logging
import os

import attr
from debut import debcon
from packageurl import PackageURL
from six import string_types

from commoncode import filetype
from commoncode import fileutils
from commoncode.datautils import List
from commoncode.datautils import String
from packagedcode import models


"""
Handle Debian packages.
"""

TRACE = False

logger = logging.getLogger(__name__)

if TRACE:
    import sys
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logger.setLevel(logging.DEBUG)


@attr.s()
class DebianPackage(models.Package):
    metafiles = ('*.control',)
    extensions = ('.deb',)
    filetypes = ('debian binary package',)
    mimetypes = ('application/x-archive', 'application/vnd.debian.binary-package',)
    default_type = 'deb'

    multi_arch = String(
        label='Multi-Arch',
        help='Multi-Arch value from status file')

    installed_files = List(
        item_type=models.PackageFile,
        label='installed files',
        help='List of files installed by this package.')

    def to_dict(self, _detailed=False, **kwargs):
        data = models.Package.to_dict(self, **kwargs)
        if _detailed:
            #################################################
            # remove temporary fields
            data['multi_arch'] = self.multi_arch
            data['installed_files'] = [istf.to_dict() for istf in (self.installed_files or [])]
            #################################################
        else:
            #################################################
            # remove temporary fields
            data.pop('multi_arch', None)
            data.pop('installed_files', None)
            #################################################

        return data

    def populate_installed_files(self, var_lib_dpkg_info_dir):
        """
        Populate the installed_file  attribute given a `var_lib_dpkg_info_dir`
        path to a Debian /var/lib/dpkg/info directory.
        """
        self.installed_files = self.get_list_of_installed_files(var_lib_dpkg_info_dir)

    def get_list_of_installed_files(self, var_lib_dpkg_info_dir):
        """
        Return a list of InstalledFile given a `var_lib_dpkg_info_dir` path to a
        Debian /var/lib/dpkg/info directory where <package>.list and/or
        <package>.md5sums files can be found for a package name.
        We first use the .md5sums file and switch to the .list file otherwise.
        The .list files also contains directories.
        """

        # Multi-Arch can be: foreign, same, allowed or empty
        # We only need to adjust the md5sum path in the case of `same`
        if self.multi_arch == 'same':
            arch = ':{}'.format(self.qualifiers.get('arch'))
        else:
            arch = ''

        package_md5sum = '{}{}.md5sums'.format(self.name, arch)
        md5sum_file = os.path.join(var_lib_dpkg_info_dir, package_md5sum)

        package_list = '{}{}.list'.format(self.name, arch)
        list_file = os.path.join(var_lib_dpkg_info_dir, package_list)

        has_md5 = os.path.exists(md5sum_file)
        has_list = os.path.exists(list_file)

        if not (has_md5 or has_list):
            return []

        installed_files = []
        directories = set()
        if has_md5:
            with open(md5sum_file) as info_file:
                for line in info_file:
                    line = line.strip()
                    if not line:
                        continue
                    md5sum, _, path = line.partition(' ')
                    md5sum = md5sum.strip()

                    path = path.strip()
                    if not path.startswith('/'):
                        path = '/' + path

                    # we ignore dirs in general, and we ignore these that would
                    # be created a plain dir when we can
                    if path in ignored_root_dirs:
                        continue

                    installed_file = models.PackageFile(path=path, md5=md5sum)

                    installed_files.append(installed_file)
                    directories.add(os.path.dirname(path))

        elif has_list:
            with open(list_file) as info_file:
                for line in info_file:
                    line = line.strip()
                    if not line:
                        continue
                    md5sum = None
                    path = line

                    path = path.strip()
                    if not path.startswith('/'):
                        path = '/' + path

                    # we ignore dirs in general, and we ignore these that would
                    # be created a plain dir when we can
                    if path in ignored_root_dirs:
                        continue

                    installed_file = models.PackageFile(path=path, md5=md5sum)
                    if installed_file not in installed_files:
                        installed_files.append(installed_file)
                    directories.add(os.path.dirname(path))

        # skip directories when possible
        installed_files = [f for f in installed_files if f.path not in directories]

        return installed_files

    def get_copyright_file_path(self, root_dir):
        """
        Given a root_dir path to a filesystem root, return the path to a copyright file
        for this Package
        """
        # We start by looking for a copyright file stored in a directory named after the
        # package name. Otherwise we look for a copyright file stored in a source package
        # name.
        candidate_names = [self.name]
        candidate_names.extend(PackageURL.from_string(sp).name for sp in self.source_packages)

        copyright_file = os.path.join(root_dir, 'usr/share/doc/{}/copyright')

        for name in candidate_names:
            copyright_loc = copyright_file.format(name)
            if os.path.exists(copyright_loc):
                return copyright_loc


def get_installed_packages(root_dir, distro='debian', detect_licenses=False, **kwargs):
    """
    Given a directory to a rootfs, yield a DebianPackage and a list of `installed_files`
    (path, md5sum) tuples.
    """

    base_status_file_loc = os.path.join(root_dir, 'var/lib/dpkg/status')
    if not os.path.exists(base_status_file_loc):
        return

    var_lib_dpkg_info_dir = os.path.join(root_dir, 'var/lib/dpkg/info/')

    # guard from recursive import
    from packagedcode import debian_copyright

    for package in parse_status_file(base_status_file_loc, distro=distro):
        package.populate_installed_files(var_lib_dpkg_info_dir)
        if detect_licenses:
            debian_copyright.get_and_set_package_licenses_and_copyrights(package, root_dir)
        yield package


def is_debian_status_file(location):
    return (filetype.is_file(location)
            and fileutils.file_name(location).lower() == 'status')


def parse_status_file(location, distro='debian'):
    """
    Yield Debian Package objects from a dpkg `status` file or None.
    """
    if not os.path.exists(location):
        raise FileNotFoundError('[Errno 2] No such file or directory: {}'.format(repr(location)))
    if not is_debian_status_file(location):
        return

    for debian_pkg_data in debcon.get_paragraphs_data_from_file(location):
        yield build_package(debian_pkg_data, distro)


def build_package(package_data, distro='debian'):
    """
    Return a Package object from a package_data mapping (from a dpkg status file)
    or None.
    """
    # construct the package
    package = DebianPackage()
    package.namespace = distro

    # add debian-specific package 'qualifiers'
    package.qualifiers = OrderedDict([
        ('arch', package_data.get('architecture')),
    ])

    # mapping of top level `status` file items to the Package object field name
    plain_fields = [
        ('description', 'description'),
        ('homepage', 'homepage_url'),
        ('installed-size', 'size'),
        ('package', 'name'),
        ('version', 'version'),
        ('maintainer', 'maintainer'),
        ('multi-arch', 'multi_arch'),
    ]

    for source, target in plain_fields:
        value = package_data.get(source)
        if value:
            if isinstance(value, string_types):
                value = value.strip()
            if value:
                setattr(package, target, value)

    # mapping of top level `status` file items to a function accepting as
    # arguments the package.json element value and returning an iterable of key,
    # values Package Object to update
    field_mappers = [
        ('section', keywords_mapper),
        ('source', source_packages_mapper),
        # ('depends', dependency_mapper),
    ]

    for source, func in field_mappers:
        logger.debug('parse: %(source)r, %(func)r' % locals())
        value = package_data.get(source) or None
        if value:
            func(value, package)

    # parties_mapper() need mutiple fields:
    parties_mapper(package_data, package)

    return package


def keywords_mapper(keyword, package):
    """
    Add `section` info as a list of keywords to a DebianPackage.
    """
    package.keywords = [keyword]
    return package


def source_packages_mapper(source, package):
    """
    Add `source` info as a list of `purl`s to a DebianPackage.
    """
    source_pkg_purl = PackageURL(
        type=package.type,
        name=source,
        namespace=package.namespace
    ).to_string()

    package.source_packages = [source_pkg_purl]

    return package


def parties_mapper(package_data, package):
    """
    add
    """
    parties = []

    maintainer = package_data.get('maintainer')
    orig_maintainer = package_data.get('original_maintainer')

    if maintainer:
        parties.append(models.Party(role='maintainer', name=maintainer))

    if orig_maintainer:
        parties.append(models.Party(role='original_maintainer', name=orig_maintainer))

    package.parties = parties

    return package


ignored_root_dirs = {
    '/.',
    '/bin',
    '/boot',
    '/cdrom',
    '/dev',
    '/etc',
    '/etc/skel',
    '/home',
    '/lib',
    '/lib32',
    '/lib64',
    '/lost+found',
    '/mnt',
    '/media',
    '/opt',
    '/proc',
    '/root',
    '/run',
    '/usr',
    '/sbin',
    '/snap',
    '/sys',
    '/tmp',
    '/usr',
    '/usr/games',
    '/usr/include',
    '/usr/sbin',
    '/usr/share/info',
    '/usr/share/man',
    '/usr/share/misc',
    '/usr/src',

    '/var',
    '/var/backups',
    '/var/cache',
    '/var/lib/dpkg',
    '/var/lib/misc',
    '/var/local',
    '/var/lock',
    '/var/log',
    '/var/opt',
    '/var/run',
    '/var/spool',
    '/var/tmp',
    '/var/lib',
}
