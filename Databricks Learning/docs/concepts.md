# Concept notes to use alongside the daily builds

Read the relevant paragraph, close it, and explain the idea using your project's observed behavior. The distinction, failure and evidence matter more than memorizing the definition.

## Days 1–5: development

**Modularity:** separate rules from environment-specific work so a change has one clear home. A pure function returns the same result for the same input without reading Spark state or writing a table. Test its contract locally; test permissions and distributed execution in the workspace.

**Packaging:** a wheel is a built Python distribution; an sdist is source plus build instructions. A wheel's compatibility tags describe where it can install. Distribution name, import name and entry-point name can differ. Check installed metadata when dispatch or imports fail.

**Bundles:** configuration describes resources, artifacts and environment differences. Validate checks configuration; deploy reconciles workspace resources; run executes a workload. The same tested code can be promoted while configuration selects a different namespace. Deployment identity, resource identity and runtime run-as identity deserve separate attention.

**Dependency scope:** code runs in an environment, not in a repository abstractly. Notebook, task and pipeline environments may differ. Resolution determines a compatible set of packages; installation puts that set into a particular environment. An import test on the driver does not prove executors can import a required library.

**UDF choice:** native Spark expressions expose more semantics to the engine. Scalar Python UDFs enable custom per-value logic; pandas UDFs process batches using Arrow and pandas. Null behavior, output types and batch length are correctness contracts. A faster wrong result is not an optimization. See the expanded Topic 1 notes for experiments.

**Testing:** unit tests isolate a small rule; integration tests exercise boundaries such as Spark types, library distribution, UC access and table writes. Output counts alone can hide wrong values. Check representative values, schema, nulls and business invariants, then run a small deployed smoke test.

## Days 6–10: ingestion and transformations

**Medallion architecture:** bronze preserves an ingestion boundary, silver applies validated business structure, and gold serves a defined analytical purpose. The layers are responsibilities, not a requirement to copy every table three times. Preserving raw context helps explain and replay transformations.

**Schema:** a schema is an agreement about fields and types. File format, parser schema, Auto Loader's stored schema and Delta's table schema are separate layers. Evolving one does not automatically prove every downstream contract remains valid. Rescued data helps investigate mismatches; it is not automatically accepted business data.

**Checkpoints:** Structured Streaming checkpoints persist progress and, for stateful queries, state needed for recovery. They do not establish business-key uniqueness. A new checkpoint can cause old input to be processed again; changing a stateful query may also make recovery incompatible.

**Declarative pipelines:** dataset functions describe a graph; the pipeline engine plans and executes it. Avoid side effects inside definitions because planning and execution may evaluate code more than once. Streaming tables maintain stream-oriented processing, while materialized views maintain query results over their source data; refresh behavior and incremental support depend on the query and source capabilities.

**Quality:** warn records a rule violation, drop removes invalid output rows, and fail stops an update when a rule is violated. Quarantine preserves invalid records for investigation. SQL predicates can be true, false or null; use an explicit null policy so every input falls into a deliberate category.

**Windows and joins:** a window can rank versions within a business key, but ordering needs deterministic tie handling. A join can multiply rows if either side has multiple matches. State the intended grain before joining and reconcile counts and revenue afterward.

**CDC and SCD:** CDC events describe source changes; a sequencing field determines which version wins even when arrival is out of order. SCD1 keeps current attributes; SCD2 retains historical intervals. Delta CDF exposes committed changes to a Delta table and is a different boundary from applying a source CDC feed.

## Days 11–16: correctness across time and services

**Watermarks:** a watermark derives progress from observed event time and a delay threshold. Stateful operations use it to bound retained state and reason about lateness. It is not a wall-clock timer or a universal command to drop all old rows. Guarantees depend on the operator and output mode.

**Output modes:** append emits newly finalized output rows, update emits changed output rows, and complete emits the full result table for supported aggregations. Choose based on the query and sink's ability to consume the output. Append of raw input is different from append of finalized window aggregates.

**Idempotency:** repeating an operation produces the same logical result as doing it once. `foreachBatch` may replay a batch, so the sink must tolerate that replay. A transaction key or appropriately designed merge can help for a particular sink; it does not create atomicity across unrelated sinks or make external side effects safe automatically.

**Orchestration:** a dependency controls when a task is eligible to run. Branches select outcomes; For Each repeats a task over parameters. Retrying a transient infrastructure failure may help; retrying deterministic bad code without a fix usually repeats the failure. Repair chooses a subset of a failed workflow but still needs valid input assumptions.

**Connect versus federation:** managed ingestion copies and incrementally maintains destination data. Federation queries an external system through a governed connection. The source can bear query load and availability requirements in federation. A replicated destination has storage and freshness costs. Choose from the actual latency, isolation and operational requirements.

**Sharing versus Clean Rooms:** sharing grants a recipient read access to chosen assets through a provider boundary. Clean Rooms support controlled collaborative computation and approved analyses. Revoking future access does not erase previous exports. Aggregate outputs still need disclosure analysis.

**VARIANT:** semi-structured values retain flexible nested structure without forcing every field into a fixed declared STRUCT upfront. Missing fields, JSON null, SQL null, type conversion failure and malformed input are different cases. Test them separately instead of treating every absent result as the same condition.

**AI enrichment:** inference adds a model-dependent interpretation, not an authoritative data-quality fact. Preserve provenance, validate output structure and labels, handle errors, and avoid repeated uncontrolled invocation. Model version, prompt and endpoint behavior belong in your reproducibility record.

**Delta history and CDF:** a transaction log gives a table a sequence of committed versions. Time travel reads a historical snapshot; CDF reads changes over a range. Update preimages and postimages are different records. Retention limits historical availability, so persist a separate audit design if long-term history is required.

## Days 17–20: performance

**Layout:** physical organization affects how many files and bytes a query reads. Partitioning splits data by directory-level key values; clustering organizes records for useful access patterns; statistics enable skipping. Many tiny files and high-cardinality partitions can cost more than they save. Measure a representative filtered workload.

**Deletion vectors:** supported table configurations can mark changed/deleted rows without immediately rewriting all affected data files. Reads must respect those marks. Deferred physical cleanup is an operational concern, and table-feature upgrades can affect reader compatibility.

**Managed maintenance:** UC managed storage gives the platform ownership of more lifecycle and optimization work. Predictive optimization can automate eligible maintenance; it does not replace a sound data model or prove a particular query is optimal. External-table designs assign more responsibility to the data owner.

**Caches:** query result caching can avoid rerunning a query; data/disk caching can avoid rereading remote bytes; Spark persistence retains chosen intermediate results. Each has a different lifetime and invalidation behavior. Record cache evidence before attributing a speed change to rewritten code or layout.

**Shuffles and skew:** a shuffle redistributes records across workers for operations such as grouping or joins. Skew makes some partitions much heavier than others, leaving straggling tasks. Broadcast can avoid shuffling a small dimension, but an oversized broadcast can create memory pressure. Fix cardinality and inspect the plan before tuning worker counts.

## Days 21–29: governance and operations

**Unity Catalog privileges:** object access depends on privileges on the object and its enclosing namespace. Inheritance can make a higher-scope grant broader than it first appears. Workspace ACLs on jobs/notebooks are a separate control plane from table/function privileges. Verify with the actual consuming identity.

**Governed functions:** session UDF registration lives within the session; a UC function is a catalog object with discovery and execution controls. Its supported language, dependencies and compute requirements still matter. A function being discoverable does not prove every user or runtime can execute it.

**Masks, filters and ABAC:** column masks transform what a querying identity sees; row filters restrict visible records. ABAC uses centrally managed policy conditions and governed tags to select enforcement across assets. The policy's scope, tag integrity and principal coverage are part of the security design. Test both allowed and denied cases.

**Pseudonymization:** hashing or tokenization can reduce direct exposure while preserving linkage. It does not automatically eliminate reidentification risk, especially for small predictable input spaces. Suppression and generalization trade information content for reduced disclosure. Choose from the use case and threat model.

**Deletion:** current rows, historical files, raw sources, downstream replicas and backups have different lifetimes. DELETE changes the logical table result; physical cleanup follows retention and supported maintenance. Source replay can restore a removed subject unless the ingestion/deletion design prevents it.

**Observability:** logs explain events; metrics summarize behavior; lineage and run identifiers connect the two. System billing usage is a measured quantity with a unit, not automatically money. Price attribution needs appropriate identifiers, effective dates and rates. An alert is useful when its threshold leads to a specific investigation or action.

**Debugging and deployment:** classify the failed boundary before changing code: syntax, data contract, dependency, privilege, resource or external service. Correlate the task error with query/pipeline evidence. Deploy a known tested revision; a repaired job should still be checked against business totals.

**Table versus file format:** Parquet describes file encoding; Delta and Iceberg add table metadata and transactional interpretation across files. A directory of Parquet files is not automatically a transactional table. Interoperability requires compatible metadata, protocol/format features, access controls and reader support.

**Dimensional grain and metric semantics:** define what one fact row represents. Historical dimensions require a valid-time match, not a join to all versions. A materialized aggregate can accelerate a known query; a metric view defines governed reusable analytical meaning. Ratios usually need correctly aggregated numerators and denominators, not an average of subgroup ratios.

**Mastery:** you can predict the output and failure boundary, implement the rule, identify evidence, repair a controlled failure, and explain when a different design is better. Recognizing the API name is only the beginning.
