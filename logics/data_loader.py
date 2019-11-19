# -*- coding: utf-8 -*-

from functools import partial
from typing import (
    Any,
    Callable,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Tuple,
    TypeVar,
)

from promise import Promise
from promise.dataloader import DataLoader

from logics.resumes import ResumesLogic
from logics.resumes.resumes_types import (  # noqa E501
    PersonalInfoLike,
    TextOnlyEnumType,
    RatableEnumType,
)
from logics.logics_utils import UUIDType

T = TypeVar("T")
IndexIdListType = List[Tuple[int, UUIDType]]
ResourceListFromIdLoaderType = List[Tuple[int, List[Optional[T]]]]
ResourceFromIdLoaderType = List[Tuple[int, Optional[T]]]
TagType = str
BatchKeyType = Tuple[TagType, UUIDType]


PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG = "0"
EDUCATION_FROM_RESUME_ID_LOADER_TAG = "1"
EXPERIENCE_FROM_RESUME_ID_LOADER_TAG = "2"
HOBBY_FROM_RESUME_ID_LOADER_TAG = "3"
SKILL_FROM_RESUME_ID_LOADER_TAG = "4"
SPOKEN_LANGUAGE_FROM_RESUME_ID_LOADER_TAG = "5"
SUPPLEMENTARY_SKILL_FROM_RESUME_ID_LOADER_TAG = "6"
ACHIEVEMENT_FROM_EDUCATION_ID_LOADER_TAG = "7"
ACHIEVEMENT_FROM_EXPERIENCE_ID_LOADER_TAG = "8"
ACHIEVEMENT_FROM_SKILL_ID_LOADER_TAG = "9"


def make_personal_info_from_resume_id_loader_hash(
    resume_id: UUIDType,
) -> BatchKeyType:  # noqa E501
    return (PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG, str(resume_id))


def make_education_from_resume_id_loader_hash(
    resume_id: UUIDType,
) -> BatchKeyType:  # noqa E501
    return (EDUCATION_FROM_RESUME_ID_LOADER_TAG, str(resume_id))


def make_experience_from_resume_id_loader_hash(
    resume_id: UUIDType,
) -> BatchKeyType:  # noqa E501
    return (EXPERIENCE_FROM_RESUME_ID_LOADER_TAG, str(resume_id))


def make_skill_from_resume_id_loader_hash(
    resume_id: UUIDType,
) -> BatchKeyType:  # noqa E501
    return (SKILL_FROM_RESUME_ID_LOADER_TAG, str(resume_id))


def make_hobby_from_resume_id_loader_hash(
    owner_id: UUIDType,
) -> BatchKeyType:  # noqa E501
    return (HOBBY_FROM_RESUME_ID_LOADER_TAG, str(owner_id))


def make_achievement_from_education_id_loader_hash(
    owner_id: UUIDType,
) -> BatchKeyType:  # noqa E501
    return (ACHIEVEMENT_FROM_EDUCATION_ID_LOADER_TAG, str(owner_id))


def make_achievement_from_experience_id_loader_hash(
    owner_id: UUIDType,
) -> BatchKeyType:
    return (ACHIEVEMENT_FROM_EXPERIENCE_ID_LOADER_TAG, str(owner_id))


def make_achievement_from_skill_id_loader_hash(
    owner_id: UUIDType,
) -> BatchKeyType:  # noqa E501
    return (ACHIEVEMENT_FROM_SKILL_ID_LOADER_TAG, str(owner_id))


def make_language_from_resume_id_loader_hash(
    owner_id: UUIDType,
) -> BatchKeyType:  # noqa E501
    return (SPOKEN_LANGUAGE_FROM_RESUME_ID_LOADER_TAG, str(owner_id))


def make_supplementary_skill_from_resume_id_loader_hash(
    owner_id: UUIDType,
) -> BatchKeyType:  # noqa E501
    return (SUPPLEMENTARY_SKILL_FROM_RESUME_ID_LOADER_TAG, str(owner_id))


def personal_info_from_resume_id_loader(
    index_resume_id_list: IndexIdListType,
) -> ResourceFromIdLoaderType[PersonalInfoLike]:
    index_personal_info_list = resources_from_from_ids_loader(
        ResumesLogic.get_personal_infos, index_resume_id_list
    )  # noqa E501

    # This is not optimal. We should not be doing a second iteration here
    return [
        (index, ps[0] if ps else None) for index, ps in index_personal_info_list
    ]  # noqa E501


def resources_from_from_ids_loader(
    resource_getter_fn: Callable[[List[UUIDType]], List[T]],
    index_arg_id_list: IndexIdListType,
    from_id_attr_name: str = "resume_id",
) -> ResourceListFromIdLoaderType[T]:
    from_ids_list: List[UUIDType] = []
    from_id_index_map: MutableMapping[UUIDType, int] = {}

    for (index, from_id) in index_arg_id_list:
        from_ids_list.append(from_id)
        from_id_index_map[from_id] = index

    from_id_to_resource_map: MutableMapping[UUIDType, List[Optional[T]]] = {}

    for p in resource_getter_fn(from_ids_list):
        from_id = str(getattr(p, from_id_attr_name))
        resources = from_id_to_resource_map.get(from_id, [])
        resources.append(p)
        from_id_to_resource_map[from_id] = resources

    index_resource_list: List[Tuple[int, List[Optional[T]]]] = []

    for from_id in from_ids_list:
        index = from_id_index_map[from_id]
        resources = from_id_to_resource_map.get(from_id, [])
        index_resource_list.append((index, resources))

    return index_resource_list


TAG_TO_RESOURCES_GETTER_FUNCTION_MAP: Mapping[  # type: ignore[disable_any_explicit] # noqa F821
    TagType, Callable[[IndexIdListType], Any]
] = {  # noqa E501
    PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG: personal_info_from_resume_id_loader,  # noqa E501
    EDUCATION_FROM_RESUME_ID_LOADER_TAG: partial(
        resources_from_from_ids_loader, ResumesLogic.get_educations
    ),
    EXPERIENCE_FROM_RESUME_ID_LOADER_TAG: partial(
        resources_from_from_ids_loader, ResumesLogic.get_experiences
    ),
    SKILL_FROM_RESUME_ID_LOADER_TAG: partial(
        resources_from_from_ids_loader, ResumesLogic.get_skills
    ),
    HOBBY_FROM_RESUME_ID_LOADER_TAG: partial(
        resources_from_from_ids_loader,
        partial(
            ResumesLogic.get_many_text_only, tag=TextOnlyEnumType.resume_hobby
        ),  # noqa E501
        from_id_attr_name="owner_id",
    ),
    ACHIEVEMENT_FROM_EDUCATION_ID_LOADER_TAG: partial(
        resources_from_from_ids_loader,
        partial(
            ResumesLogic.get_many_text_only,
            tag=TextOnlyEnumType.education_achievement,  # noqa E501
        ),
        from_id_attr_name="owner_id",
    ),
    ACHIEVEMENT_FROM_EXPERIENCE_ID_LOADER_TAG: partial(
        resources_from_from_ids_loader,
        partial(
            ResumesLogic.get_many_text_only,
            tag=TextOnlyEnumType.experience_achievement,  # noqa E501
        ),
        from_id_attr_name="owner_id",
    ),
    ACHIEVEMENT_FROM_SKILL_ID_LOADER_TAG: partial(
        resources_from_from_ids_loader,
        partial(
            ResumesLogic.get_many_text_only,
            tag=TextOnlyEnumType.skill_achievement,  # noqa E501
        ),
        from_id_attr_name="owner_id",
    ),
    SPOKEN_LANGUAGE_FROM_RESUME_ID_LOADER_TAG: partial(
        resources_from_from_ids_loader,
        partial(
            ResumesLogic.get_ratables, tag=RatableEnumType.spoken_language,  # noqa E501
        ),
        from_id_attr_name="owner_id",
    ),
    SUPPLEMENTARY_SKILL_FROM_RESUME_ID_LOADER_TAG: partial(
        resources_from_from_ids_loader,
        partial(
            ResumesLogic.get_ratables,
            tag=RatableEnumType.supplementary_skill,  # noqa E501
        ),
        from_id_attr_name="owner_id",
    ),
}


class AppDataLoader(DataLoader):
    def batch_load_fn(self, keys: List[BatchKeyType]) -> None:
        tags_index_args_map: MutableMapping[
            TagType, List[Tuple[int, UUIDType]]
        ] = {}  # noqa E501

        for index, key in enumerate(keys):
            tag, args = key
            index_args_list = tags_index_args_map.get(tag, [])
            index_args_list.append((index, args))
            tags_index_args_map[tag] = index_args_list

        index_resource_list: List[Tuple[int, Any]] = []  # type: ignore

        for tag in tags_index_args_map:
            index_args_list = tags_index_args_map[tag]

            index_resource_list.extend(
                TAG_TO_RESOURCES_GETTER_FUNCTION_MAP[tag](index_args_list)
            )  # noqa E502

        return Promise.resolve(
            [
                resource[1]
                for resource in sorted(
                    index_resource_list, key=lambda member: member[0]
                )
            ]
        )
