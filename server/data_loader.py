# -*- coding: utf-8 -*-

from typing import (  # noqa E501
    Any,
    Callable,
    List,
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
from server.apps.resumes.resumes_commons import EducationLike, PersonalInfoLike

T = TypeVar("T")
IndexIdListType = List[Tuple[int, str]]
ResourceListFromIdLoaderType = List[Tuple[int, List[Optional[T]]]]
ResourceFromIdLoaderType = List[Tuple[int, Optional[T]]]


class HasResumeId(Protocol):
    resume_id: str


TAG_ARGS_SEPARATOR = "::"
PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG = "0"
EDUCATION_FROM_RESUME_ID_LOADER_TAG = "1"
EXPERIENCE_FROM_RESUME_ID_LOADER_TAG = "2"
HOBBY_FROM_RESUME_ID_LOADER_TAG = "3"
SKILL_FROM_RESUME_ID_LOADER_TAG = "4"
SPOKEN_LANGUAGE_FROM_RESUME_ID_LOADER_TAG = "5"
SUPPLEMENTARY_SKILL_FROM_RESUME_ID_LOADER_TAG = "6"


def make_personal_info_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> str:  # noqa E501
    resume_id = str(resume_id)

    return "{}{}{}".format(
        PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG, TAG_ARGS_SEPARATOR, resume_id
    )


def make_education_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> str:  # noqa E501
    resume_id = str(resume_id)
    return (
        f"{EDUCATION_FROM_RESUME_ID_LOADER_TAG}{TAG_ARGS_SEPARATOR}{resume_id}"
    )  # noqa


def make_experience_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> str:  # noqa
    resume_id = str(resume_id)
    return (
        f"{EDUCATION_FROM_RESUME_ID_LOADER_TAG}{TAG_ARGS_SEPARATOR}{resume_id}"
    )  # noqa E501


def make_skill_from_resume_id_loader_hash(resume_id: Union[UUID, str]) -> str:
    resume_id = str(resume_id)
    return f"{SKILL_FROM_RESUME_ID_LOADER_TAG}{TAG_ARGS_SEPARATOR}{resume_id}"


def personal_info_from_resume_id_loader(
    index_resume_id_list: IndexIdListType
) -> ResourceFromIdLoaderType[PersonalInfoLike]:
    index_personal_info_list = from_resume_id_loader(
        index_resume_id_list, ResumesLogic.get_personal_infos
    )  # noqa E501

    # This is not optimal. We should not be doing a second iteration here
    return [
        (index, ps[0] if ps else None) for index, ps in index_personal_info_list
    ]  # noqa E501


def education_from_resume_id_loader(
    index_resume_id_list: IndexIdListType
) -> ResourceListFromIdLoaderType[EducationLike]:
    return from_resume_id_loader(
        index_resume_id_list, ResumesLogic.get_educations
    )  # noqa E501


def from_resume_id_loader(
    index_resume_id_list: IndexIdListType,
    resource_getter_fn: Callable[[List[str]], List[T]],
) -> ResourceListFromIdLoaderType[T]:
    resume_ids_list: List[str] = []
    resume_id_index_map: MutableMapping[str, int] = {}

    for (index, resume_id) in index_resume_id_list:
        resume_ids_list.append(resume_id)
        resume_id_index_map[resume_id] = index

    resume_id_resource_map: MutableMapping[str, List[Optional[T]]] = {}

    for p in resource_getter_fn(resume_ids_list):
        resume_id = str(cast(HasResumeId, p).resume_id)
        resources = resume_id_resource_map.get(resume_id, [])
        resources.append(p)
        resume_id_resource_map[resume_id] = resources

    index_resource_list: List[Tuple[int, List[Optional[T]]]] = []

    for resume_id in resume_ids_list:
        index = resume_id_index_map[resume_id]
        resources = resume_id_resource_map.get(resume_id, [])
        index_resource_list.append((index, resources))

    return index_resource_list


class AppDataLoader(DataLoader):
    def batch_load_fn(self, keys: List[str]) -> None:
        tags_index_args_map: MutableMapping[str, List[Tuple[int, str]]] = {}

        for index, key in enumerate(keys):
            tag, args = key.split(TAG_ARGS_SEPARATOR, 2)
            index_args_list = tags_index_args_map.get(tag, [])
            index_args_list.append((index, args))
            tags_index_args_map[tag] = index_args_list

        index_resource_list: List[Tuple[int, Any]] = []  # type: ignore

        for tag in tags_index_args_map:
            index_args_list = tags_index_args_map[tag]

            if tag == PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG:
                index_resource_list.extend(
                    personal_info_from_resume_id_loader(index_args_list)
                )  # noqa

            elif tag == EDUCATION_FROM_RESUME_ID_LOADER_TAG:
                index_resource_list.extend(
                    education_from_resume_id_loader(index_args_list)
                )
        return Promise.resolve(
            [
                resource[1]
                for resource in sorted(
                    index_resource_list, key=lambda member: member[0]
                )
            ]
        )
