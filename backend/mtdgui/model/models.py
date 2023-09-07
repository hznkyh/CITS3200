from pydantic import BaseModel
from typing import List, Dict, Tuple, Union

# class Constants(BaseModel):
#     OS_TYPES: List[str]
#     OS_VERSION_DICT: Dict[str, List[str]]
#     HOST_TAGS: List[str]
#     NODE_COLOURS: List[str]
#     SERVICE_VERSIONS: List[int]
#     LARGE_INT: int

#     USER_TO_NODES_RATIO: int
#     USER_PROB_TO_REUSE_PASS: float
#     USER_TOTAL_FOR_EACH_HOST: int

#     HOST_SERVICES_MIN: int
#     HOST_SERVICES_MAX: int
#     HOST_INTERNAL_SERVICE_MIN: int
#     HOST_PORT_RANGE: List[int]
#     HOST_MAX_PROB_FOR_USER_COMPROMISE: float

#     VULN_MAX_PROB_FOR_OCCURING_FOR_SERVICE_VERSION: float
#     VULN_INITIAL_CHANCES: int
#     VULN_PATCH_MEAN: int
#     VULN_PATCH_RANGE: int
#     VULN_PERCENT_CROSS_PLATFORM: float
#     VULN_PROB_DEPENDS_ON_OS: float
#     VULN_PROB_DEPENDS_ON_OTHER_VULNS: float
#     VULN_MIN_EXPLOIT_TIME: int
#     VULN_MAX_EXPLOIT_TIME: int
#     VULN_MIN_COMPLEXITY: float

#     SERVICE_NO_OF_SERVICES_PER_OS: int
#     SERVICE_COMPROMISED_THRESHOLD: int
#     SERVICE_DISCOVER_EACH_VULN_TIME: int
#     SERVICE_TOP_X_VULNS_TO_RETURN: int

#     HACKER_ATTACK_ATTEMPT_MULTIPLER: int

#     STANDARD_ERROR_BENCHMARK_PERCENT: int
#     ATTACKER_THRESHOLD: int

#     MTD_TRIGGER_INTERVAL: Dict[str, Tuple[int, float]]
#     MTD_PRIORITY: Dict[str, int]
#     MTD_DURATION: Dict[str, Tuple[int, float]]

#     ATTACK_DURATION: Dict[str, int]

#     class Config:
#         arbitrary_types_allowed = True


class Constants(BaseModel):
    OS_TYPES: List[str]
    OS_VERSION_DICT: Dict[str, List[str]]
    HOST_TAGS: List[str]
    NODE_COLOURS: List[str]
    SERVICE_VERSIONS: List[int]
    LARGE_INT: str
    USER_TO_NODES_RATIO: int
    USER_PROB_TO_REUSE_PASS: float
    USER_TOTAL_FOR_EACH_HOST: int
    HOST_SERVICES_MIN: int
    HOST_SERVICES_MAX: int
    HOST_INTERNAL_SERVICE_MIN: int
    HOST_PORT_RANGE: str
    HOST_MAX_PROB_FOR_USER_COMPROMISE: float
    VULN_MAX_PROB_FOR_OCCURING_FOR_SERVICE_VERSION: float
    VULN_INITIAL_CHANCES: int
    VULN_PATCH_MEAN: int
    VULN_PATCH_RANGE: int
    VULN_PERCENT_CROSS_PLATFORM: float
    VULN_PROB_DEPENDS_ON_OS: float
    VULN_PROB_DEPENDS_ON_OTHER_VULNS: float
    VULN_MIN_EXPLOIT_TIME: int
    VULN_MAX_EXPLOIT_TIME: int
    VULN_MIN_COMPLEXITY: float
    SERVICE_NO_OF_SERVICES_PER_OS: int
    SERVICE_COMPROMISED_THRESHOLD: int
    SERVICE_DISCOVER_EACH_VULN_TIME: int
    SERVICE_TOP_X_VULNS_TO_RETURN: int
    HACKER_ATTACK_ATTEMPT_MULTIPLER: int
    STANDARD_ERROR_BENCHMARK_PERCENT: int
    ATTACKER_THRESHOLD: int
    MTD_TRIGGER_INTERVAL: Dict[str, List[Union[int, float]]]
    MTD_PRIORITY: Dict[str, int]
    MTD_DURATION: Dict[str, List[Union[int, float]]]
    ATTACK_DURATION: Dict[str, int]