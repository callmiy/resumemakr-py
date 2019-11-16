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
    Union,
    cast,
)
from uuid import UUID

from promise import Promise
from promise.dataloader import DataLoader
from typing_extensions import Protocol

from server.apps.resumes.logic import ResumesLogic
from server.apps.resumes.resumes_commons import PersonalInfoLike


T = TypeVar("T")
IndexIdListType = List[Tuple[int, str]]
ResourceListFromIdLoaderType = List[Tuple[int, List[Optional[T]]]]
ResourceFromIdLoaderType = List[Tuple[int, Optional[T]]]
TagType = str
LoaderHashType = Tuple[TagType, str]
BatchKeysType = Tuple[TagType, List[str]]


class HasResumeId(Protocol):
    resume_id: str


PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG = (
    "0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)

EDUCATION_FROM_RESUME_ID_LOADER_TAG = "1"
EXPERIENCE_FROM_RESUME_ID_LOADER_TAG = "2"
HOBBY_FROM_RESUME_ID_LOADER_TAG = "3"
SKILL_FROM_RESUME_ID_LOADER_TAG = "4"
SPOKEN_LANGUAGE_FROM_RESUME_ID_LOADER_TAG = "5"
SUPPLEMENTARY_SKILL_FROM_RESUME_ID_LOADER_TAG = "6"


def make_personal_info_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> LoaderHashType:
    return (PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG, str(resume_id))


def make_education_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> LoaderHashType:
    return (EDUCATION_FROM_RESUME_ID_LOADER_TAG, str(resume_id))


def make_experience_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> LoaderHashType:
    return (EDUCATION_FROM_RESUME_ID_LOADER_TAG, str(resume_id))


def make_skill_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> LoaderHashType:
    return (SKILL_FROM_RESUME_ID_LOADER_TAG, str(resume_id))


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
    resource_getter_fn: Callable[[List[str]], List[T]],
    index_arg_id_list: IndexIdListType,
) -> ResourceListFromIdLoaderType[T]:
    resume_ids_list: List[str] = []
    resume_id_index_map: MutableMapping[str, int] = {}

    for (index, arg_id) in index_arg_id_list:
        resume_ids_list.append(arg_id)
        resume_id_index_map[arg_id] = index

    resume_id_resource_map: MutableMapping[str, List[Optional[T]]] = {}

    for p in resource_getter_fn(resume_ids_list):
        arg_id = str(cast(HasResumeId, p).resume_id)
        resources = resume_id_resource_map.get(arg_id, [])
        resources.append(p)
        resume_id_resource_map[arg_id] = resources

    index_resource_list: List[Tuple[int, List[Optional[T]]]] = []

    for arg_id in resume_ids_list:
        index = resume_id_index_map[arg_id]
        resources = resume_id_resource_map.get(arg_id, [])
        index_resource_list.append((index, resources))

    return index_resource_list


resources_getter_fn_map: Mapping[  # type: ignore[disable_any_explicit] # noqa F821
    TagType, Callable[[IndexIdListType], Any]
] = {  # noqa E501
    PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG: personal_info_from_resume_id_loader,  # noqa E501
    EDUCATION_FROM_RESUME_ID_LOADER_TAG: partial(
        resources_from_from_ids_loader, ResumesLogic.get_educations
    ),
    SKILL_FROM_RESUME_ID_LOADER_TAG: partial(
        resources_from_from_ids_loader, ResumesLogic.get_skills
    ),
}


class AppDataLoader(DataLoader):
    def batch_load_fn(self, keys: BatchKeysType) -> None:
        tags_index_args_map: MutableMapping[TagType, List[Tuple[int, str]]] = {}

        for index, key in enumerate(keys):
            tag, args = key
            index_args_list = tags_index_args_map.get(tag, [])
            index_args_list.append((index, args))
            tags_index_args_map[tag] = index_args_list

        index_resource_list: List[Tuple[int, Any]] = []  # type: ignore

        for tag in tags_index_args_map:
            index_args_list = tags_index_args_map[tag]

            index_resource_list.extend(
                resources_getter_fn_map[tag](index_args_list)
            )  # noqa E502

        return Promise.resolve(
            [
                resource[1]
                for resource in sorted(
                    index_resource_list, key=lambda member: member[0]
                )
            ]
        )
