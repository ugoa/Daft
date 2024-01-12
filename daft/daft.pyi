import builtins
from enum import Enum
from typing import Any, Callable

from daft.runners.partitioning import PartitionCacheEntry
from daft.execution import physical_plan
from daft.plan_scheduler.physical_plan_scheduler import PartitionT
import pyarrow
from daft.io.scan import ScanOperator

class ImageMode(Enum):
    """
    Supported image modes for Daft's image type.
    """

    #: 8-bit grayscale
    L: int

    #: 8-bit grayscale + alpha
    LA: int

    #: 8-bit RGB
    RGB: int

    #: 8-bit RGB + alpha
    RGBA: int

    #: 16-bit grayscale
    L16: int

    #: 16-bit grayscale + alpha
    LA16: int

    #: 16-bit RGB
    RGB16: int

    #: 16-bit RGB + alpha
    RGBA16: int

    #: 32-bit floating RGB
    RGB32F: int

    #: 32-bit floating RGB + alpha
    RGBA32F: int

    @staticmethod
    def from_mode_string(mode: str) -> ImageMode:
        """
        Create an ImageMode from its string representation.

        Args:
            mode: String representation of the mode. This is the same as the enum
                attribute name, e.g. ``ImageMode.from_mode_string("RGB")`` would
                return ``ImageMode.RGB``.
        """
        ...

class ImageFormat(Enum):
    """
    Supported image formats for Daft's image I/O.
    """

    PNG: int
    JPEG: int
    TIFF: int
    GIF: int
    BMP: int

    @staticmethod
    def from_format_string(mode: str) -> ImageFormat:
        """
        Create an ImageFormat from its string representation.
        """
        ...

class JoinType(Enum):
    """
    Type of a join operation.
    """

    Inner: int
    Left: int
    Right: int

    @staticmethod
    def from_join_type_str(join_type: str) -> JoinType:
        """
        Create a JoinType from its string representation.

        Args:
            join_type: String representation of the join type. This is the same as the enum
                attribute name, e.g. ``JoinType.from_join_type_str("Inner")`` would
                return ``JoinType.Inner``.
        """
        ...

class CountMode(Enum):
    """
    Supported count modes for Daft's count aggregation.

    | All   - Count both non-null and null values.
    | Valid - Count only valid values.
    | Null  - Count only null values.
    """

    All: int
    Valid: int
    Null: int

    @staticmethod
    def from_count_mode_str(count_mode: str) -> CountMode:
        """
        Create a CountMode from its string representation.

        Args:
            count_mode: String representation of the count mode , e.g. "all", "valid", or "null".
        """
        ...

class PartitionScheme(Enum):
    """
    Partition scheme for Daft DataFrame.
    """

    Range: int
    Hash: int
    Random: int
    Unknown: int

class PartitionSpec:
    """
    Partition specification for a Daft DataFrame.
    """

    scheme: PartitionScheme
    num_partitions: int
    by: list[PyExpr]

    def __init__(
        self, scheme: PartitionScheme = PartitionScheme.Unknown, num_partitions: int = 0, by: list[PyExpr] | None = None
    ): ...
    def __eq__(self, other: PartitionSpec) -> bool: ...  # type: ignore[override]
    def __ne__(self, other: PartitionSpec) -> bool: ...  # type: ignore[override]
    def __str__(self) -> str: ...

class ResourceRequest:
    """
    Resource request for a query fragment task.
    """

    num_cpus: float | None
    num_gpus: float | None
    memory_bytes: int | None

    def __init__(
        self, num_cpus: float | None = None, num_gpus: float | None = None, memory_bytes: int | None = None
    ): ...
    @staticmethod
    def max_resources(resource_requests: list[ResourceRequest]):
        """Take a field-wise max of the list of resource requests."""
        ...
    def __add__(self, other: ResourceRequest) -> ResourceRequest: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: ResourceRequest) -> bool: ...  # type: ignore[override]
    def __ne__(self, other: ResourceRequest) -> bool: ...  # type: ignore[override]

class FileFormat(Enum):
    """
    Format of a file, e.g. Parquet, CSV, and JSON.
    """

    Parquet: int
    Csv: int
    Json: int

class ParquetSourceConfig:
    """
    Configuration of a Parquet data source.
    """

    def __init__(self, coerce_int96_timestamp_unit: PyTimeUnit | None = None): ...

class CsvSourceConfig:
    """
    Configuration of a CSV data source.
    """

    delimiter: str | None
    has_headers: bool
    double_quote: bool
    quote: str | None
    escape_char: str | None
    comment: str | None
    buffer_size: int | None
    chunk_size: int | None

    def __init__(
        self,
        has_headers: bool,
        double_quote: bool,
        delimiter: str | None,
        quote: str | None,
        escape_char: str | None,
        comment: str | None,
        buffer_size: int | None = None,
        chunk_size: int | None = None,
    ): ...

class JsonSourceConfig:
    """
    Configuration of a JSON data source.
    """

    buffer_size: int | None
    chunk_size: int | None

    def __init__(
        self,
        buffer_size: int | None = None,
        chunk_size: int | None = None,
    ): ...

class FileFormatConfig:
    """
    Configuration for parsing a particular file format (Parquet, CSV, JSON).
    """

    config: ParquetSourceConfig | CsvSourceConfig | JsonSourceConfig

    @staticmethod
    def from_parquet_config(config: ParquetSourceConfig) -> FileFormatConfig:
        """
        Create a Parquet file format config.
        """
        ...
    @staticmethod
    def from_csv_config(config: CsvSourceConfig) -> FileFormatConfig:
        """
        Create a CSV file format config.
        """
        ...
    @staticmethod
    def from_json_config(config: JsonSourceConfig) -> FileFormatConfig:
        """
        Create a JSON file format config.
        """
        ...
    def file_format(self) -> FileFormat:
        """
        Get the file format for this config.
        """
        ...
    def __eq__(self, other: FileFormatConfig) -> bool: ...  # type: ignore[override]
    def __ne__(self, other: FileFormatConfig) -> bool: ...  # type: ignore[override]

class CsvConvertOptions:
    """
    Options for converting CSV data to Daft data.
    """

    limit: int | None
    include_columns: list[str] | None
    column_names: list[str] | None
    schema: PySchema | None
    predicate: PyExpr | None

    def __init__(
        self,
        limit: int | None = None,
        include_columns: list[str] | None = None,
        column_names: list[str] | None = None,
        schema: PySchema | None = None,
        predicate: PyExpr | None = None,
    ): ...

class CsvParseOptions:
    """
    Options for parsing CSV files.
    """

    has_header: bool
    delimiter: str | None
    double_quote: bool
    quote: str | None
    escape_char: str | None
    comment: str | None

    def __init__(
        self,
        has_header: bool = True,
        delimiter: str | None = None,
        double_quote: bool = True,
        quote: str | None = None,
        escape_char: str | None = None,
        comment: str | None = None,
    ): ...

class CsvReadOptions:
    """
    Options for reading CSV files.
    """

    buffer_size: int | None
    chunk_size: int | None

    def __init__(
        self,
        buffer_size: int | None = None,
        chunk_size: int | None = None,
    ): ...

class JsonConvertOptions:
    """
    Options for converting JSON data to Daft data.
    """

    limit: int | None
    include_columns: list[str] | None
    schema: PySchema | None

    def __init__(
        self,
        limit: int | None = None,
        include_columns: list[str] | None = None,
        schema: PySchema | None = None,
    ): ...

class JsonParseOptions:
    """
    Options for parsing JSON files.
    """

class JsonReadOptions:
    """
    Options for reading JSON files.
    """

    buffer_size: int | None
    chunk_size: int | None

    def __init__(
        self,
        buffer_size: int | None = None,
        chunk_size: int | None = None,
    ): ...

class FileInfo:
    """
    Metadata for a single file.
    """

    file_path: str
    file_size: int | None
    num_rows: int | None

class FileInfos:
    """
    Metadata for a collection of files.
    """

    file_paths: list[str]
    file_sizes: list[int | None]
    num_rows: list[int | None]

    @staticmethod
    def from_infos(file_paths: list[str], file_sizes: list[int | None], num_rows: list[int | None]) -> FileInfos: ...
    @staticmethod
    def from_table(table: PyTable) -> FileInfos:
        """
        Create from a Daft table with "path", "size", and "num_rows" columns.
        """
        ...
    def extend(self, new_infos: FileInfos) -> FileInfos:
        """
        Concatenate two FileInfos together.
        """
        ...
    def __getitem__(self, idx: int) -> FileInfo: ...
    def to_table(self) -> PyTable:
        """
        Convert to a Daft table with "path", "size", and "num_rows" columns.
        """
    def __len__(self) -> int: ...

class S3Config:
    """
    I/O configuration for accessing an S3-compatible system.
    """

    region_name: str | None
    endpoint_url: str | None
    key_id: str | None
    session_token: str | None
    access_key: str | None
    max_connections: int
    retry_initial_backoff_ms: int
    connect_timeout_ms: int
    read_timeout_ms: int
    num_tries: int
    retry_mode: str | None
    anonymous: bool
    verify_ssl: bool
    check_hostname_ssl: bool

    def __init__(
        self,
        region_name: str | None = None,
        endpoint_url: str | None = None,
        key_id: str | None = None,
        session_token: str | None = None,
        access_key: str | None = None,
        max_connections: int | None = None,
        retry_initial_backoff_ms: int | None = None,
        connect_timeout_ms: int | None = None,
        read_timeout_ms: int | None = None,
        num_tries: int | None = None,
        retry_mode: str | None = None,
        anonymous: bool | None = None,
        verify_ssl: bool | None = None,
        check_hostname_ssl: bool | None = None,
    ): ...
    def replace(
        self,
        region_name: str | None = None,
        endpoint_url: str | None = None,
        key_id: str | None = None,
        session_token: str | None = None,
        access_key: str | None = None,
        max_connections: int | None = None,
        retry_initial_backoff_ms: int | None = None,
        connect_timeout_ms: int | None = None,
        read_timeout_ms: int | None = None,
        num_tries: int | None = None,
        retry_mode: str | None = None,
        anonymous: bool | None = None,
        verify_ssl: bool | None = None,
        check_hostname_ssl: bool | None = None,
    ) -> S3Config:
        """Replaces values if provided, returning a new S3Config"""
        ...

class AzureConfig:
    """
    I/O configuration for accessing Azure Blob Storage.
    """

    def __init__(
        self, storage_account: str | None = None, access_key: str | None = None, anonymous: str | None = None
    ): ...
    def replace(
        self, storage_account: str | None = None, access_key: str | None = None, anonymous: str | None = None
    ) -> AzureConfig:
        """Replaces values if provided, returning a new AzureConfig"""
        ...

class GCSConfig:
    """
    I/O configuration for accessing Google Cloud Storage.
    """

    project_id: str | None
    anonymous: bool

    def __init__(self, project_id: str | None = None, anonymous: bool | None = None): ...
    def replace(self, project_id: str | None = None, anonymous: bool | None = None) -> GCSConfig:
        """Replaces values if provided, returning a new GCSConfig"""
        ...

class IOConfig:
    """
    Configuration for the native I/O layer, e.g. credentials for accessing cloud storage systems.
    """

    s3: S3Config
    azure: AzureConfig
    gcs: GCSConfig

    def __init__(self, s3: S3Config | None = None, azure: AzureConfig | None = None, gcs: GCSConfig | None = None): ...
    @staticmethod
    def from_json(input: str) -> IOConfig:
        """
        Recreate an IOConfig from a JSON string.
        """
    def replace(
        self, s3: S3Config | None = None, azure: AzureConfig | None = None, gcs: GCSConfig | None = None
    ) -> IOConfig:
        """Replaces values if provided, returning a new IOConfig"""
        ...

class NativeStorageConfig:
    """
    Storage configuration for the Rust-native I/O layer.
    """

    # Whether or not to use a multithreaded tokio runtime for processing I/O
    multithreaded_io: bool
    io_config: IOConfig

    def __init__(self, multithreaded_io: bool, io_config: IOConfig): ...

class PythonStorageConfig:
    """
    Storage configuration for the legacy Python I/O layer.
    """

    io_config: IOConfig

    def __init__(self, io_config: IOConfig): ...

class StorageConfig:
    """
    Configuration for interacting with a particular storage backend, using a particular
    I/O layer implementation.
    """

    @staticmethod
    def native(config: NativeStorageConfig) -> StorageConfig:
        """
        Create from a native storage config.
        """
        ...
    @staticmethod
    def python(config: PythonStorageConfig) -> StorageConfig:
        """
        Create from a Python storage config.
        """
        ...
    @property
    def config(self) -> NativeStorageConfig | PythonStorageConfig: ...

class ScanTask:
    """
    A batch of scan tasks for reading data from an external source.
    """

    def num_rows(self) -> int:
        """
        Get number of rows that will be scanned by this ScanTask.
        """
        ...
    def size_bytes(self) -> int:
        """
        Get number of bytes that will be scanned by this ScanTask.
        """
        ...
    @staticmethod
    def catalog_scan_task(
        file: str,
        file_format: FileFormatConfig,
        schema: PySchema,
        num_rows: int,
        storage_config: StorageConfig,
        size_bytes: int | None,
        pushdowns: Pushdowns | None,
        partition_values: PyTable | None,
    ) -> ScanTask | None:
        """
        Create a Catalog Scan Task
        """
        ...

class ScanOperatorHandle:
    """
    A handle to a scan operator.
    """

    @staticmethod
    def anonymous_scan(
        files: list[str],
        schema: PySchema,
        file_format_config: FileFormatConfig,
        storage_config: StorageConfig,
    ) -> ScanOperatorHandle: ...
    @staticmethod
    def glob_scan(
        glob_path: list[str],
        file_format_config: FileFormatConfig,
        storage_config: StorageConfig,
        schema_hint: PySchema | None = None,
    ) -> ScanOperatorHandle: ...
    @staticmethod
    def from_python_scan_operator(operator: ScanOperator) -> ScanOperatorHandle: ...

class PartitionField:
    """
    Partitioning Field of a Scan Source such as Hive or Iceberg
    """

    field: PyField

    def __init__(
        self, field: PyField, source_field: PyField | None = None, transform: PartitionTransform | None = None
    ) -> None: ...

class PartitionTransform:
    """
    Partitioning Transform from a Data Catalog source field to a Partitioning Columns
    """

    @staticmethod
    def identity() -> PartitionTransform: ...
    @staticmethod
    def year() -> PartitionTransform: ...
    @staticmethod
    def month() -> PartitionTransform: ...
    @staticmethod
    def day() -> PartitionTransform: ...
    @staticmethod
    def hour() -> PartitionTransform: ...
    @staticmethod
    def iceberg_bucket(n: int) -> PartitionTransform: ...

class Pushdowns:
    """
    Pushdowns from the query optimizer that can optimize scanning data sources.
    """

    columns: list[str] | None
    filters: PyExpr | None
    partition_filters: PyExpr | None
    limit: int | None

def read_parquet(
    uri: str,
    columns: list[str] | None = None,
    start_offset: int | None = None,
    num_rows: int | None = None,
    row_groups: list[int] | None = None,
    predicate: PyExpr | None = None,
    io_config: IOConfig | None = None,
    multithreaded_io: bool | None = None,
    coerce_int96_timestamp_unit: PyTimeUnit | None = None,
): ...
def read_parquet_bulk(
    uris: list[str],
    columns: list[str] | None = None,
    start_offset: int | None = None,
    num_rows: int | None = None,
    row_groups: list[list[int] | None] | None = None,
    predicate: PyExpr | None = None,
    io_config: IOConfig | None = None,
    num_parallel_tasks: int | None = 128,
    multithreaded_io: bool | None = None,
    coerce_int96_timestamp_unit: PyTimeUnit | None = None,
): ...
def read_parquet_statistics(
    uris: PySeries,
    io_config: IOConfig | None = None,
    multithreaded_io: bool | None = None,
): ...
def read_parquet_into_pyarrow(
    uri: str,
    columns: list[str] | None = None,
    start_offset: int | None = None,
    num_rows: int | None = None,
    row_groups: list[int] | None = None,
    io_config: IOConfig | None = None,
    multithreaded_io: bool | None = None,
    coerce_int96_timestamp_unit: PyTimeUnit | None = None,
): ...
def read_parquet_into_pyarrow_bulk(
    uris: list[str],
    columns: list[str] | None = None,
    start_offset: int | None = None,
    num_rows: int | None = None,
    row_groups: list[list[int] | None] | None = None,
    io_config: IOConfig | None = None,
    num_parallel_tasks: int | None = 128,
    multithreaded_io: bool | None = None,
    coerce_int96_timestamp_unit: PyTimeUnit | None = None,
): ...
def read_parquet_schema(
    uri: str,
    io_config: IOConfig | None = None,
    multithreaded_io: bool | None = None,
    coerce_int96_timestamp_unit: PyTimeUnit | None = None,
): ...
def read_csv(
    uri: str,
    convert_options: CsvConvertOptions | None = None,
    parse_options: CsvParseOptions | None = None,
    read_options: CsvReadOptions | None = None,
    io_config: IOConfig | None = None,
    multithreaded_io: bool | None = None,
): ...
def read_csv_schema(
    uri: str,
    parse_options: CsvParseOptions | None = None,
    io_config: IOConfig | None = None,
    multithreaded_io: bool | None = None,
): ...
def read_json(
    uri: str,
    convert_options: JsonConvertOptions | None = None,
    parse_options: JsonParseOptions | None = None,
    read_options: JsonReadOptions | None = None,
    io_config: IOConfig | None = None,
    multithreaded_io: bool | None = None,
    max_chunks_in_flight: int | None = None,
): ...
def read_json_schema(
    uri: str,
    parse_options: JsonParseOptions | None = None,
    io_config: IOConfig | None = None,
    multithreaded_io: bool | None = None,
): ...

class PyTimeUnit:
    @staticmethod
    def nanoseconds() -> PyTimeUnit: ...
    @staticmethod
    def microseconds() -> PyTimeUnit: ...
    @staticmethod
    def milliseconds() -> PyTimeUnit: ...
    @staticmethod
    def seconds() -> PyTimeUnit: ...

class PyDataType:
    @staticmethod
    def null() -> PyDataType: ...
    @staticmethod
    def bool() -> PyDataType: ...
    @staticmethod
    def int8() -> PyDataType: ...
    @staticmethod
    def int16() -> PyDataType: ...
    @staticmethod
    def int32() -> PyDataType: ...
    @staticmethod
    def int64() -> PyDataType: ...
    @staticmethod
    def uint8() -> PyDataType: ...
    @staticmethod
    def uint16() -> PyDataType: ...
    @staticmethod
    def uint32() -> PyDataType: ...
    @staticmethod
    def uint64() -> PyDataType: ...
    @staticmethod
    def float32() -> PyDataType: ...
    @staticmethod
    def float64() -> PyDataType: ...
    @staticmethod
    def binary() -> PyDataType: ...
    @staticmethod
    def string() -> PyDataType: ...
    @staticmethod
    def decimal128(precision: int, size: int) -> PyDataType: ...
    @staticmethod
    def date() -> PyDataType: ...
    @staticmethod
    def timestamp(time_unit: PyTimeUnit, timezone: str | None = None) -> PyDataType: ...
    @staticmethod
    def duration(time_unit: PyTimeUnit) -> PyDataType: ...
    @staticmethod
    def list(data_type: PyDataType) -> PyDataType: ...
    @staticmethod
    def fixed_size_list(data_type: PyDataType, size: int) -> PyDataType: ...
    @staticmethod
    def struct(fields: dict[str, PyDataType]) -> PyDataType: ...
    @staticmethod
    def extension(name: str, storage_data_type: PyDataType, metadata: str | None = None) -> PyDataType: ...
    @staticmethod
    def embedding(data_type: PyDataType, size: int) -> PyDataType: ...
    @staticmethod
    def image(mode: ImageMode | None = None, height: int | None = None, width: int | None = None) -> PyDataType: ...
    @staticmethod
    def tensor(dtype: PyDataType, shape: tuple[int, ...] | None = None) -> PyDataType: ...
    @staticmethod
    def python() -> PyDataType: ...
    def to_arrow(self, cast_tensor_type_for_ray: builtins.bool | None = None) -> pyarrow.DataType: ...
    def is_image(self) -> builtins.bool: ...
    def is_fixed_shape_image(self) -> builtins.bool: ...
    def is_tensor(self) -> builtins.bool: ...
    def is_fixed_shape_tensor(self) -> builtins.bool: ...
    def is_logical(self) -> builtins.bool: ...
    def is_temporal(self) -> builtins.bool: ...
    def is_equal(self, other: Any) -> builtins.bool: ...
    @staticmethod
    def from_json(serialized: str) -> PyDataType: ...
    def __reduce__(self) -> tuple: ...
    def __hash__(self) -> int: ...

class PyField:
    def name(self) -> str: ...
    @staticmethod
    def create(name: str, datatype: PyDataType) -> PyField: ...
    def dtype(self) -> PyDataType: ...
    def eq(self, other: PyField) -> bool: ...
    def __reduce__(self) -> tuple: ...

class PySchema:
    def __getitem__(self, name: str) -> PyField: ...
    def names(self) -> list[str]: ...
    def union(self, other: PySchema) -> PySchema: ...
    def apply_hints(self, other: PySchema) -> PySchema: ...
    def eq(self, other: PySchema) -> bool: ...
    @staticmethod
    def from_field_name_and_types(names_and_types: list[tuple[str, PyDataType]]) -> PySchema: ...
    @staticmethod
    def from_fields(fields: list[PyField]) -> PySchema: ...
    def __reduce__(self) -> tuple: ...
    def __repr__(self) -> str: ...
    def _repr_html_(self) -> str: ...

class PyExpr:
    def _input_mapping(self) -> str | None: ...
    def _required_columns(self) -> set[str]: ...
    def _is_column(self) -> bool: ...
    def alias(self, name: str) -> PyExpr: ...
    def cast(self, dtype: PyDataType) -> PyExpr: ...
    def if_else(self, if_true: PyExpr, if_false: PyExpr) -> PyExpr: ...
    def count(self, mode: CountMode) -> PyExpr: ...
    def sum(self) -> PyExpr: ...
    def mean(self) -> PyExpr: ...
    def min(self) -> PyExpr: ...
    def max(self) -> PyExpr: ...
    def agg_list(self) -> PyExpr: ...
    def agg_concat(self) -> PyExpr: ...
    def explode(self) -> PyExpr: ...
    def __abs__(self) -> PyExpr: ...
    def __add__(self, other: PyExpr) -> PyExpr: ...
    def __sub__(self, other: PyExpr) -> PyExpr: ...
    def __mul__(self, other: PyExpr) -> PyExpr: ...
    def __floordiv__(self, other: PyExpr) -> PyExpr: ...
    def __truediv__(self, other: PyExpr) -> PyExpr: ...
    def __mod__(self, other: PyExpr) -> PyExpr: ...
    def __and__(self, other: PyExpr) -> PyExpr: ...
    def __or__(self, other: PyExpr) -> PyExpr: ...
    def __xor__(self, other: PyExpr) -> PyExpr: ...
    def __invert__(self) -> PyExpr: ...
    def __lt__(self, other: PyExpr) -> PyExpr: ...
    def __le__(self, other: PyExpr) -> PyExpr: ...
    def __gt__(self, other: PyExpr) -> PyExpr: ...
    def __ge__(self, other: PyExpr) -> PyExpr: ...
    def __eq__(self, other: PyExpr) -> PyExpr: ...  # type: ignore[override]
    def __ne__(self, other: PyExpr) -> PyExpr: ...  # type: ignore[override]
    def is_null(self) -> PyExpr: ...
    def not_null(self) -> PyExpr: ...
    def name(self) -> str: ...
    def to_field(self, schema: PySchema) -> PyField: ...
    def __repr__(self) -> str: ...
    def __hash__(self) -> int: ...
    def __reduce__(self) -> tuple: ...
    def is_nan(self) -> PyExpr: ...
    def dt_date(self) -> PyExpr: ...
    def dt_day(self) -> PyExpr: ...
    def dt_hour(self) -> PyExpr: ...
    def dt_month(self) -> PyExpr: ...
    def dt_year(self) -> PyExpr: ...
    def dt_day_of_week(self) -> PyExpr: ...
    def utf8_endswith(self, pattern: PyExpr) -> PyExpr: ...
    def utf8_startswith(self, pattern: PyExpr) -> PyExpr: ...
    def utf8_contains(self, pattern: PyExpr) -> PyExpr: ...
    def utf8_split(self, pattern: PyExpr) -> PyExpr: ...
    def utf8_length(self) -> PyExpr: ...
    def image_decode(self) -> PyExpr: ...
    def image_encode(self, image_format: ImageFormat) -> PyExpr: ...
    def image_resize(self, w: int, h: int) -> PyExpr: ...
    def image_crop(self, bbox: PyExpr) -> PyExpr: ...
    def list_join(self, delimiter: PyExpr) -> PyExpr: ...
    def list_lengths(self) -> PyExpr: ...
    def list_get(self, idx: PyExpr, default: PyExpr) -> PyExpr: ...
    def struct_get(self, name: str) -> PyExpr: ...
    def url_download(
        self, max_connections: int, raise_error_on_failure: bool, multi_thread: bool, config: IOConfig
    ) -> PyExpr: ...

def eq(expr1: PyExpr, expr2: PyExpr) -> bool: ...
def col(name: str) -> PyExpr: ...
def lit(item: Any) -> PyExpr: ...
def date_lit(item: int) -> PyExpr: ...
def timestamp_lit(item: int, tu: PyTimeUnit, tz: str | None) -> PyExpr: ...
def udf(func: Callable, expressions: list[PyExpr], return_dtype: PyDataType) -> PyExpr: ...

class PySeries:
    @staticmethod
    def from_arrow(name: str, pyarrow_array: pyarrow.Array) -> PySeries: ...
    @staticmethod
    def from_pylist(name: str, pylist: list[Any], pyobj: str) -> PySeries: ...
    def to_pylist(self) -> list[Any]: ...
    def to_arrow(self) -> pyarrow.Array: ...
    def __abs__(self) -> PySeries: ...
    def __add__(self, other: PySeries) -> PySeries: ...
    def __sub__(self, other: PySeries) -> PySeries: ...
    def __mul__(self, other: PySeries) -> PySeries: ...
    def __truediv__(self, other: PySeries) -> PySeries: ...
    def __mod__(self, other: PySeries) -> PySeries: ...
    def __and__(self, other: PySeries) -> PySeries: ...
    def __or__(self, other: PySeries) -> PySeries: ...
    def __xor__(self, other: PySeries) -> PySeries: ...
    def __lt__(self, other: PySeries) -> PySeries: ...
    def __le__(self, other: PySeries) -> PySeries: ...
    def __gt__(self, other: PySeries) -> PySeries: ...
    def __ge__(self, other: PySeries) -> PySeries: ...
    def __eq__(self, other: PySeries) -> PySeries: ...  # type: ignore[override]
    def __ne__(self, other: PySeries) -> PySeries: ...  # type: ignore[override]
    def take(self, idx: PySeries) -> PySeries: ...
    def slice(self, start: int, end: int) -> PySeries: ...
    def filter(self, mask: PySeries) -> PySeries: ...
    def sort(self, descending: bool) -> PySeries: ...
    def argsort(self, descending: bool) -> PySeries: ...
    def hash(self, seed: PySeries | None = None) -> PySeries: ...
    def __invert__(self) -> PySeries: ...
    def _count(self, mode: CountMode) -> PySeries: ...
    def _sum(self) -> PySeries: ...
    def _mean(self) -> PySeries: ...
    def _min(self) -> PySeries: ...
    def _max(self) -> PySeries: ...
    def _agg_list(self) -> PySeries: ...
    def cast(self, dtype: PyDataType) -> PySeries: ...
    @staticmethod
    def concat(series: list[PySeries]) -> PySeries: ...
    def __len__(self) -> int: ...
    def size_bytes(self) -> int: ...
    def name(self) -> str: ...
    def rename(self, name: str) -> PySeries: ...
    def data_type(self) -> PyDataType: ...
    def utf8_endswith(self, pattern: PySeries) -> PySeries: ...
    def utf8_startswith(self, pattern: PySeries) -> PySeries: ...
    def utf8_contains(self, pattern: PySeries) -> PySeries: ...
    def utf8_split(self, pattern: PySeries) -> PySeries: ...
    def utf8_length(self) -> PySeries: ...
    def is_nan(self) -> PySeries: ...
    def dt_date(self) -> PySeries: ...
    def dt_day(self) -> PySeries: ...
    def dt_hour(self) -> PySeries: ...
    def dt_month(self) -> PySeries: ...
    def dt_year(self) -> PySeries: ...
    def dt_day_of_week(self) -> PySeries: ...
    def partitioning_days(self) -> PySeries: ...
    def partitioning_hours(self) -> PySeries: ...
    def partitioning_months(self) -> PySeries: ...
    def partitioning_years(self) -> PySeries: ...
    def partitioning_iceberg_bucket(self, n: int) -> PySeries: ...
    def list_lengths(self) -> PySeries: ...
    def list_get(self, idx: PySeries, default: PySeries) -> PySeries: ...
    def image_decode(self) -> PySeries: ...
    def image_encode(self, image_format: ImageFormat) -> PySeries: ...
    def image_resize(self, w: int, h: int) -> PySeries: ...
    def if_else(self, other: PySeries, predicate: PySeries) -> PySeries: ...
    def is_null(self) -> PySeries: ...
    def not_null(self) -> PySeries: ...
    def murmur3_32(self) -> PySeries: ...
    def _debug_bincode_serialize(self) -> bytes: ...
    @staticmethod
    def _debug_bincode_deserialize(b: bytes) -> PySeries: ...

class PyTable:
    def schema(self) -> PySchema: ...
    def cast_to_schema(self, schema: PySchema) -> PyTable: ...
    def eval_expression_list(self, exprs: list[PyExpr]) -> PyTable: ...
    def take(self, idx: PySeries) -> PyTable: ...
    def filter(self, exprs: list[PyExpr]) -> PyTable: ...
    def sort(self, sort_keys: list[PyExpr], descending: list[bool]) -> PyTable: ...
    def argsort(self, sort_keys: list[PyExpr], descending: list[bool]) -> PySeries: ...
    def agg(self, to_agg: list[PyExpr], group_by: list[PyExpr]) -> PyTable: ...
    def join(self, right: PyTable, left_on: list[PyExpr], right_on: list[PyExpr]) -> PyTable: ...
    def explode(self, to_explode: list[PyExpr]) -> PyTable: ...
    def head(self, num: int) -> PyTable: ...
    def sample_by_fraction(self, fraction: float, with_replacement: bool, seed: int | None) -> PyTable: ...
    def sample_by_size(self, size: int, with_replacement: bool, seed: int | None) -> PyTable: ...
    def quantiles(self, num: int) -> PyTable: ...
    def partition_by_hash(self, exprs: list[PyExpr], num_partitions: int) -> list[PyTable]: ...
    def partition_by_random(self, num_partitions: int, seed: int) -> list[PyTable]: ...
    def partition_by_range(
        self, partition_keys: list[PyExpr], boundaries: PyTable, descending: list[bool]
    ) -> list[PyTable]: ...
    def __repr__(self) -> str: ...
    def _repr_html_(self) -> str: ...
    def __len__(self) -> int: ...
    def size_bytes(self) -> int: ...
    def column_names(self) -> list[str]: ...
    def get_column(self, name: str) -> PySeries: ...
    def get_column_by_index(self, idx: int) -> PySeries: ...
    @staticmethod
    def concat(tables: list[PyTable]) -> PyTable: ...
    def slice(self, start: int, end: int) -> PyTable: ...
    @staticmethod
    def from_arrow_record_batches(record_batches: list[pyarrow.RecordBatch], schema: PySchema) -> PyTable: ...
    @staticmethod
    def from_pylist_series(dict: dict[str, PySeries]) -> PyTable: ...
    def to_arrow_record_batch(self) -> pyarrow.RecordBatch: ...
    @staticmethod
    def empty(schema: PySchema | None = None) -> PyTable: ...

class PyMicroPartition:
    def schema(self) -> PySchema: ...
    def column_names(self) -> list[str]: ...
    def get_column(self, name: str) -> PySeries: ...
    def size_bytes(self) -> int | None: ...
    def _repr_html_(self) -> str: ...
    @staticmethod
    def empty(schema: PySchema | None = None) -> PyMicroPartition: ...
    @staticmethod
    def from_scan_task(scan_task: ScanTask) -> PyMicroPartition: ...
    @staticmethod
    def from_tables(tables: list[PyTable]) -> PyMicroPartition: ...
    @staticmethod
    def from_arrow_record_batches(record_batches: list[pyarrow.RecordBatch], schema: PySchema) -> PyMicroPartition: ...
    @staticmethod
    def concat(tables: list[PyMicroPartition]) -> PyMicroPartition: ...
    def slice(self, start: int, end: int) -> PyMicroPartition: ...
    def to_table(self) -> PyTable: ...
    def cast_to_schema(self, schema: PySchema) -> PyMicroPartition: ...
    def eval_expression_list(self, exprs: list[PyExpr]) -> PyMicroPartition: ...
    def take(self, idx: PySeries) -> PyMicroPartition: ...
    def filter(self, exprs: list[PyExpr]) -> PyMicroPartition: ...
    def sort(self, sort_keys: list[PyExpr], descending: list[bool]) -> PyMicroPartition: ...
    def argsort(self, sort_keys: list[PyExpr], descending: list[bool]) -> PySeries: ...
    def agg(self, to_agg: list[PyExpr], group_by: list[PyExpr]) -> PyMicroPartition: ...
    def join(self, right: PyMicroPartition, left_on: list[PyExpr], right_on: list[PyExpr]) -> PyMicroPartition: ...
    def explode(self, to_explode: list[PyExpr]) -> PyMicroPartition: ...
    def head(self, num: int) -> PyMicroPartition: ...
    def sample_by_fraction(self, fraction: float, with_replacement: bool, seed: int | None) -> PyMicroPartition: ...
    def sample_by_size(self, size: int, with_replacement: bool, seed: int | None) -> PyMicroPartition: ...
    def quantiles(self, num: int) -> PyMicroPartition: ...
    def partition_by_hash(self, exprs: list[PyExpr], num_partitions: int) -> list[PyMicroPartition]: ...
    def partition_by_random(self, num_partitions: int, seed: int) -> list[PyMicroPartition]: ...
    def partition_by_range(
        self, partition_keys: list[PyExpr], boundaries: PyTable, descending: list[bool]
    ) -> list[PyMicroPartition]: ...
    def __repr__(self) -> str: ...
    def __len__(self) -> int: ...
    @classmethod
    def read_parquet(
        cls,
        path: str,
        columns: list[str] | None = None,
        start_offset: int | None = None,
        num_rows: int | None = None,
        row_groups: list[int] | None = None,
        predicate: PyExpr | None = None,
        io_config: IOConfig | None = None,
        multithreaded_io: bool | None = None,
        coerce_int96_timestamp_unit: PyTimeUnit = PyTimeUnit.nanoseconds(),
    ): ...
    @classmethod
    def read_parquet_bulk(
        cls,
        uris: list[str],
        columns: list[str] | None = None,
        start_offset: int | None = None,
        num_rows: int | None = None,
        row_groups: list[list[int] | None] | None = None,
        predicate: PyExpr | None = None,
        io_config: IOConfig | None = None,
        num_parallel_tasks: int | None = None,
        multithreaded_io: bool | None = None,
        coerce_int96_timestamp_unit: PyTimeUnit | None = None,
    ): ...
    @classmethod
    def read_csv(
        cls,
        uri: str,
        convert_options: CsvConvertOptions | None = None,
        parse_options: CsvParseOptions | None = None,
        read_options: CsvReadOptions | None = None,
        io_config: IOConfig | None = None,
        multithreaded_io: bool | None = None,
    ): ...
    @classmethod
    def read_json_native(
        cls,
        uri: str,
        convert_options: JsonConvertOptions | None = None,
        parse_options: JsonParseOptions | None = None,
        read_options: JsonReadOptions | None = None,
        io_config: IOConfig | None = None,
        multithreaded_io: bool | None = None,
    ): ...

class PhysicalPlanScheduler:
    """
    A work scheduler for physical query plans.
    """

    def num_partitions(self) -> int: ...
    def to_partition_tasks(
        self, psets: dict[str, list[PartitionT]], is_ray_runner: bool
    ) -> physical_plan.InProgressPhysicalPlan: ...

class LogicalPlanBuilder:
    """
    A logical plan builder, which simplifies constructing logical plans via
    a fluent interface. E.g., LogicalPlanBuilder.table_scan(..).project(..).filter(..).

    This builder holds the current root (sink) of the logical plan, and the building methods return
    a brand new builder holding a new plan; i.e., this is an immutable builder.
    """

    @staticmethod
    def in_memory_scan(
        partition_key: str, cache_entry: PartitionCacheEntry, schema: PySchema, num_partitions: int, size_bytes: int
    ) -> LogicalPlanBuilder: ...
    @staticmethod
    def table_scan_with_scan_operator(scan_operator: ScanOperatorHandle) -> LogicalPlanBuilder: ...
    @staticmethod
    def table_scan(
        file_infos: FileInfos, schema: PySchema, file_format_config: FileFormatConfig, storage_config: StorageConfig
    ) -> LogicalPlanBuilder: ...
    def project(self, projection: list[PyExpr], resource_request: ResourceRequest) -> LogicalPlanBuilder: ...
    def filter(self, predicate: PyExpr) -> LogicalPlanBuilder: ...
    def limit(self, limit: int, eager: bool) -> LogicalPlanBuilder: ...
    def explode(self, to_explode: list[PyExpr]) -> LogicalPlanBuilder: ...
    def sort(self, sort_by: list[PyExpr], descending: list[bool]) -> LogicalPlanBuilder: ...
    def repartition(
        self,
        partition_by: list[PyExpr],
        scheme: PartitionScheme,
        num_partitions: int | None,
    ) -> LogicalPlanBuilder: ...
    def coalesce(self, num_partitions: int) -> LogicalPlanBuilder: ...
    def distinct(self) -> LogicalPlanBuilder: ...
    def sample(self, fraction: float, with_replacement: bool, seed: int | None) -> LogicalPlanBuilder: ...
    def aggregate(self, agg_exprs: list[PyExpr], groupby_exprs: list[PyExpr]) -> LogicalPlanBuilder: ...
    def join(
        self, right: LogicalPlanBuilder, left_on: list[PyExpr], right_on: list[PyExpr], join_type: JoinType
    ) -> LogicalPlanBuilder: ...
    def concat(self, other: LogicalPlanBuilder) -> LogicalPlanBuilder: ...
    def table_write(
        self,
        root_dir: str,
        file_format: FileFormat,
        partition_cols: list[PyExpr] | None = None,
        compression: str | None = None,
        io_config: IOConfig | None = None,
    ) -> LogicalPlanBuilder: ...
    def schema(self) -> PySchema: ...
    def optimize(self) -> LogicalPlanBuilder: ...
    def to_physical_plan_scheduler(self, cfg: PyDaftExecutionConfig) -> PhysicalPlanScheduler: ...
    def repr_ascii(self, simple: bool) -> str: ...

class PyDaftExecutionConfig:
    def with_config_values(
        self,
        merge_scan_tasks_min_size_bytes: int | None = None,
        merge_scan_tasks_max_size_bytes: int | None = None,
        broadcast_join_size_bytes_threshold: int | None = None,
    ) -> PyDaftExecutionConfig: ...
    @property
    def merge_scan_tasks_min_size_bytes(self) -> int: ...
    @property
    def merge_scan_tasks_max_size_bytes(self): ...
    @property
    def broadcast_join_size_bytes_threshold(self): ...
    @property
    def sample_size_for_sort(self): ...

class PyDaftPlanningConfig:
    def with_config_values(
        self,
        default_io_config: IOConfig | None = None,
    ) -> PyDaftPlanningConfig: ...
    @property
    def default_io_config(self) -> IOConfig: ...

def build_type() -> str: ...
def version() -> str: ...
def __getattr__(name) -> Any: ...
def io_glob(
    path: str,
    multithreaded_io: bool | None = None,
    io_config: IOConfig | None = None,
    fanout_limit: int | None = None,
    page_size: int | None = None,
    limit: int | None = None,
) -> list[dict]: ...
