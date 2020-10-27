import glob
import os

from .utils import list_dir
from .folder import make_dataset
from .video_utils import VideoClips
from .vision import VisionDataset


class HMDB51(VisionDataset):
    """
    `HMDB51 <http://serre-lab.clps.brown.edu/resource/hmdb-a-large-human-motion-database/>`_
    dataset.

    HMDB51 is an action recognition video dataset.
    This dataset consider every video as a collection of video clips of fixed size, specified
    by ``frames_per_clip``, where the step in frames between each clip is given by
    ``step_between_clips``.

    To give an example, for 2 videos with 10 and 15 frames respectively, if ``frames_per_clip=5``
    and ``step_between_clips=5``, the dataset size will be (2 + 3) = 5, where the first two
    elements will come from video 1, and the next three elements from video 2.
    Note that we drop clips which do not have exactly ``frames_per_clip`` elements, so not all
    frames in a video might be present.

    Internally, it uses a VideoClips object to handle clip creation.

    Args:
        root (string): Root directory of the HMDB51 Dataset.
        annotation_path (str): Path to the folder containing the split files.
        frames_per_clip (int): Number of frames in a clip.
        step_between_clips (int): Number of frames between each clip.
        fold (int, optional): Which fold to use. Should be between 1 and 3.
        train (bool, optional): If ``True``, creates a dataset from the train split,
            otherwise from the ``test`` split.
        transform (callable, optional): A function/transform that takes in a TxHxWxC video
            and returns a transformed version.

    Returns:
        video (Tensor[T, H, W, C]): the `T` video frames
        audio(Tensor[K, L]): the audio frames, where `K` is the number of channels
            and `L` is the number of points
        label (int): class of the video clip
    """

    data_url = "http://serre-lab.clps.brown.edu/wp-content/uploads/2013/10/hmdb51_org.rar"
    splits = {
        "url": "http://serre-lab.clps.brown.edu/wp-content/uploads/2013/10/test_train_splits.rar",
        "md5": "15e67781e70dcfbdce2d7dbb9b3344b5"
    }
    TRAIN_TAG = 1
    TEST_TAG = 2

    def __init__(self, root, annotation_path, frames_per_clip, step_between_clips=1,
                 frame_rate=None, fold=1, train=True, transform=None,
                 _precomputed_metadata=None, num_workers=1, _video_width=0,
                 _video_height=0, _video_min_dimension=0, _audio_samples=0):
        super(HMDB51, self).__init__(root)
        if fold not in (1, 2, 3):
            raise ValueError("fold should be between 1 and 3, got {}".format(fold))

        extensions = ('avi',)
        classes = sorted(list_dir(root))
        class_to_idx = {class_: i for (i, class_) in enumerate(classes)}
        self.samples = make_dataset(
            self.root,
            class_to_idx,
            extensions,
        )

        video_paths = [path for (path, _) in self.samples]
        video_clips = VideoClips(
            video_paths,
            frames_per_clip,
            step_between_clips,
            frame_rate,
            _precomputed_metadata,
            num_workers=num_workers,
            _video_width=_video_width,
            _video_height=_video_height,
            _video_min_dimension=_video_min_dimension,
            _audio_samples=_audio_samples,
        )
        self.fold = fold
        self.train = train
        self.classes = classes
        self.video_clips_metadata = video_clips.metadata
        self.indices = self._select_fold(video_paths, annotation_path, fold, train)
        self.video_clips = video_clips.subset(self.indices)
        self.transform = transform

    @property
    def metadata(self):
        return self.video_clips_metadata

    def _select_fold(self, video_list, annotations_dir, fold, train):
        target_tag = self.TRAIN_TAG if train else self.TEST_TAG
        split_pattern_name = "*test_split{}.txt".format(fold)
        split_pattern_path = os.path.join(annotations_dir, split_pattern_name)
        annotation_paths = glob.glob(split_pattern_path)
        selected_files = []
        for filepath in annotation_paths:
            with open(filepath) as fid:
                lines = fid.readlines()
            for line in lines:
                video_filename, tag_string = line.split()
                tag = int(tag_string)
                if tag == target_tag:
                    selected_files.append(video_filename)
        selected_files = set(selected_files)

        indices = []
        for video_index, video_path in enumerate(video_list):
            if os.path.basename(video_path) in selected_files:
                indices.append(video_index)

        return indices

    def __len__(self):
        return self.video_clips.num_clips()

    def __getitem__(self, idx):
        video, audio, _, video_idx = self.video_clips.get_clip(idx)
        sample_index = self.indices[video_idx]
        _, class_index = self.samples[sample_index]

        if self.transform is not None:
            video = self.transform(video)

        return video, audio, class_index
