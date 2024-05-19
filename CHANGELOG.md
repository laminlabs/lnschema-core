# Changelog

<!-- prettier-ignore -->
Name | PR | Developer | Date | Version
--- | --- | --- | --- | ---
🚚 Reformulate data lineage, remove json field from run | [385](https://github.com/laminlabs/lnschema-core/pull/385) | [falexwolf](https://github.com/falexwolf) | 2024-05-19 | 0.67.0
♻️ Protect feature in FeatureSet | [384](https://github.com/laminlabs/lnschema-core/pull/384) | [falexwolf](https://github.com/falexwolf) | 2024-05-18 |
🏗️ Naming conventions for link tables, protecting deletion in link tables, maintaining integrity upon label & feature renames | [383](https://github.com/laminlabs/lnschema-core/pull/383) | [falexwolf](https://github.com/falexwolf) | 2024-05-18 |
🚚 Rename `.type` to `.dtype` for `Feature` and `FeatureSet` | [382](https://github.com/laminlabs/lnschema-core/pull/382) | [falexwolf](https://github.com/falexwolf) | 2024-05-17 |
🔥 Prune migrations | [381](https://github.com/laminlabs/lnschema-core/pull/381) | [falexwolf](https://github.com/falexwolf) | 2024-05-16 |
🔥 Delete old migrations and create a new squashed initial migration | [380](https://github.com/laminlabs/lnschema-core/pull/380) | [falexwolf](https://github.com/falexwolf) | 2024-05-16 |
✨ Add `FeatureValue` and `ParamValue` | [379](https://github.com/laminlabs/lnschema-core/pull/379) | [falexwolf](https://github.com/falexwolf) | 2024-05-15 |
Add using docstring | [378](https://github.com/laminlabs/lnschema-core/pull/378) | [Zethson](https://github.com/Zethson) | 2024-05-07 |
♻️ Move `version` field into `IsVersioned` base model | [377](https://github.com/laminlabs/lnschema-core/pull/377) | [falexwolf](https://github.com/falexwolf) | 2024-05-07 |
📝 Better examples for FeatureSet | [375](https://github.com/laminlabs/lnschema-core/pull/375) | [sunnyosun](https://github.com/sunnyosun) | 2024-05-06 |
✨ Add an `instance_uid` field to Storage | [374](https://github.com/laminlabs/lnschema-core/pull/374) | [falexwolf](https://github.com/falexwolf) | 2024-04-28 | 0.66.0
✨ Allow passing path to .from_anndata | [373](https://github.com/laminlabs/lnschema-core/pull/373) | [sunnyosun](https://github.com/sunnyosun) | 2024-04-23 |
🚑️ Fix public_source in inspect | [372](https://github.com/laminlabs/lnschema-core/pull/372) | [sunnyosun](https://github.com/sunnyosun) | 2024-04-18 |
🐛 Fix replicated outputs slot | [371](https://github.com/laminlabs/lnschema-core/pull/371) | [falexwolf](https://github.com/falexwolf) | 2024-04-17 | 0.65.0
🚚 Rename `.stage()` to `.cache()`, add `.save(upload=None)` | [369](https://github.com/laminlabs/lnschema-core/pull/369) | [falexwolf](https://github.com/falexwolf) | 2024-04-16 |
🚚 Add `Run.replicated_outputs` & `Transform.ulabels` | [370](https://github.com/laminlabs/lnschema-core/pull/370) | [falexwolf](https://github.com/falexwolf) | 2024-04-16 |
📝 Update signature and docs for Collection.mapped | [367](https://github.com/laminlabs/lnschema-core/pull/367) | [Koncopd](https://github.com/Koncopd) | 2024-04-12 | 0.64.11
🚸 Eliminate kwargs | [366](https://github.com/laminlabs/lnschema-core/pull/366) | [sunnyosun](https://github.com/sunnyosun) | 2024-04-11 |
✨ Add from_mudata | [365](https://github.com/laminlabs/lnschema-core/pull/365) | [sunnyosun](https://github.com/sunnyosun) | 2024-04-10 | 0.64.7
♻️ Replace TypeVar with TypeAlias | [363](https://github.com/laminlabs/lnschema-core/pull/363) | [falexwolf](https://github.com/falexwolf) | 2024-04-04 | 0.64.6
📝 Fix manual type annotations in docstrings | [362](https://github.com/laminlabs/lnschema-core/pull/362) | [falexwolf](https://github.com/falexwolf) | 2024-04-04 | 0.64.5
Future annotations | [361](https://github.com/laminlabs/lnschema-core/pull/361) | [Zethson](https://github.com/Zethson) | 2024-04-04 |
✨ Introduce Registry.get() | [360](https://github.com/laminlabs/lnschema-core/pull/360) | [falexwolf](https://github.com/falexwolf) | 2024-03-30 | 0.64.4
✅ Add test for string equivalency of transform types | [359](https://github.com/laminlabs/lnschema-core/pull/359) | [falexwolf](https://github.com/falexwolf) | 2024-03-30 | 0.64.3
🔥 No collections from anndata or df anymore | [358](https://github.com/laminlabs/lnschema-core/pull/358) | [falexwolf](https://github.com/falexwolf) | 2024-03-28 | 0.64.2
✨ Collection stage | [357](https://github.com/laminlabs/lnschema-core/pull/357) | [Koncopd](https://github.com/Koncopd) | 2024-03-25 | 0.64.1
📝 Clarify the transform docs | [356](https://github.com/laminlabs/lnschema-core/pull/356) | [falexwolf](https://github.com/falexwolf) | 2024-03-19 |
♻️ Add a json field to run | [355](https://github.com/laminlabs/lnschema-core/pull/355) | [falexwolf](https://github.com/falexwolf) | 2024-03-17 | 0.64.0
🚚 Rename `run_at` to `started_at` for `Run`, add `finished_at` | [354](https://github.com/laminlabs/lnschema-core/pull/354) | [falexwolf](https://github.com/falexwolf) | 2024-03-15 |
🚚 Add `.description` to `Transform` & rename `short_name` to `key`, char field fixes | [353](https://github.com/laminlabs/lnschema-core/pull/353) | [falexwolf](https://github.com/falexwolf) | 2024-03-15 |
🚸 More sensible transform types | [352](https://github.com/laminlabs/lnschema-core/pull/352) | [falexwolf](https://github.com/falexwolf) | 2024-03-09 | 0.63.0
🏷️ Replace PathLike with UPathStr | [351](https://github.com/laminlabs/lnschema-core/pull/351) | [falexwolf](https://github.com/falexwolf) | 2024-03-05 | 0.62.1
🚚 Rename dev to core | [349](https://github.com/laminlabs/lnschema-core/pull/349) | [falexwolf](https://github.com/falexwolf) | 2024-02-29 |
✨ Add unknown_label to Collection.mapped signature | [345](https://github.com/laminlabs/lnschema-core/pull/345) | [Koncopd](https://github.com/Koncopd) | 2024-02-27 |
🚚 Use var_field for anndata | [348](https://github.com/laminlabs/lnschema-core/pull/348) | [sunnyosun](https://github.com/sunnyosun) | 2024-02-27 |
🚸 Simplify features linking | [347](https://github.com/laminlabs/lnschema-core/pull/347) | [sunnyosun](https://github.com/sunnyosun) | 2024-02-27 |
🎨 Decouple features from Artifact construction | [344](https://github.com/laminlabs/lnschema-core/pull/344) | [sunnyosun](https://github.com/sunnyosun) | 2024-02-26 |
Add registries docstring | [346](https://github.com/laminlabs/lnschema-core/pull/346) | [Zethson](https://github.com/Zethson) | 2024-02-26 |
💚 Fix docs | [343](https://github.com/laminlabs/lnschema-core/pull/343) | [sunnyosun](https://github.com/sunnyosun) | 2024-01-31 |
📝 Fix docstrings | [342](https://github.com/laminlabs/lnschema-core/pull/342) | [sunnyosun](https://github.com/sunnyosun) | 2024-01-31 |
📝 Update docstring to use bionty | [340](https://github.com/laminlabs/lnschema-core/pull/340) | [sunnyosun](https://github.com/sunnyosun) | 2024-01-30 | 0.61.3
✨ Add add_to_version_family | [338](https://github.com/laminlabs/lnschema-core/pull/338) | [sunnyosun](https://github.com/sunnyosun) | 2024-01-29 | 0.61.2
📝 Update collection.delete signature | [336](https://github.com/laminlabs/lnschema-core/pull/336) | [sunnyosun](https://github.com/sunnyosun) | 2024-01-26 |
🚚 Rename .bionty to .public | [335](https://github.com/laminlabs/lnschema-core/pull/335) | [sunnyosun](https://github.com/sunnyosun) | 2024-01-09 |
🚸 Order `.df()` by `updated_at` | [334](https://github.com/laminlabs/lnschema-core/pull/334) | [falexwolf](https://github.com/falexwolf) | 2024-01-08 |
🎨 Order artifact collections | [333](https://github.com/laminlabs/lnschema-core/pull/333) | [falexwolf](https://github.com/falexwolf) | 2024-01-07 | 0.61.0
📝 Explain join_vars="auto" in Collection.mapped | [332](https://github.com/laminlabs/lnschema-core/pull/332) | [Koncopd](https://github.com/Koncopd) | 2024-01-07 |
✨ Add outer join and categories caching to Collection.mapped | [331](https://github.com/laminlabs/lnschema-core/pull/331) | [Koncopd](https://github.com/Koncopd) | 2024-01-02 | 0.60.1
🚚 Rename `Dataset` to `Collection` | [330](https://github.com/laminlabs/lnschema-core/pull/330) | [falexwolf](https://github.com/falexwolf) | 2023-12-23 | 0.60.0
🚚 Add field description to storage | [329](https://github.com/laminlabs/lnschema-core/pull/329) | [falexwolf](https://github.com/falexwolf) | 2023-12-23 |
🔥 Remove initial_version_id | [328](https://github.com/laminlabs/lnschema-core/pull/328) | [falexwolf](https://github.com/falexwolf) | 2023-12-23 |
🚚 Add environment foreign key | [324](https://github.com/laminlabs/lnschema-core/pull/324) | [falexwolf](https://github.com/falexwolf) | 2023-12-21 | 0.59.0
♻️ Add n_objects and n_observations to Artifact and remove unique constraint for key, storage | [323](https://github.com/laminlabs/lnschema-core/pull/323) | [falexwolf](https://github.com/falexwolf) | 2023-12-12 | 0.58.1
🔥 Remove field storage from dataset | [322](https://github.com/laminlabs/lnschema-core/pull/322) | [falexwolf](https://github.com/falexwolf) | 2023-12-11 | 0.58.0
🚚 Rename File to Artifact | [321](https://github.com/laminlabs/lnschema-core/pull/321) | [falexwolf](https://github.com/falexwolf) | 2023-12-11 |
✨ Do virtual inner join of variables in Dataset.mapped | [320](https://github.com/laminlabs/lnschema-core/pull/320) | [Koncopd](https://github.com/Koncopd) | 2023-12-05 |
💚 Fix docstring | [319](https://github.com/laminlabs/lnschema-core/pull/319) | [sunnyosun](https://github.com/sunnyosun) | 2023-12-02 |
📝 Enabled ID conversion via return_field | [318](https://github.com/laminlabs/lnschema-core/pull/318) | [sunnyosun](https://github.com/sunnyosun) | 2023-12-02 |
✨ Added view_tree for keys | [317](https://github.com/laminlabs/lnschema-core/pull/317) | [sunnyosun](https://github.com/sunnyosun) | 2023-11-24 |
🚚 Recode visibility | [316](https://github.com/laminlabs/lnschema-core/pull/316) | [sunnyosun](https://github.com/sunnyosun) | 2023-11-23 |
🚚 Rename indexed to mapped | [315](https://github.com/laminlabs/lnschema-core/pull/315) | [falexwolf](https://github.com/falexwolf) | 2023-11-20 | 0.57.1
🚸 Add `.df()` to `Registry` | [314](https://github.com/laminlabs/lnschema-core/pull/314) | [falexwolf](https://github.com/falexwolf) | 2023-11-20 | 0.57.0
✨ Initial implementation of IndexedDataset | [313](https://github.com/laminlabs/lnschema-core/pull/313) | [Koncopd](https://github.com/Koncopd) | 2023-11-20 |
🔥 Remove `Modality` | [312](https://github.com/laminlabs/lnschema-core/pull/312) | [sunnyosun](https://github.com/sunnyosun) | 2023-11-13 |
✏️ Fix VisibilityChoice | [311](https://github.com/laminlabs/lnschema-core/pull/311) | [sunnyosun](https://github.com/sunnyosun) | 2023-11-13 |
🚚 Add key_is_virtual field to File | [310](https://github.com/laminlabs/lnschema-core/pull/310) | [falexwolf](https://github.com/falexwolf) | 2023-10-27 | 0.54.0
♻️ Create using method | [309](https://github.com/laminlabs/lnschema-core/pull/309) | [falexwolf](https://github.com/falexwolf) | 2023-10-27 |
✨ Add `visibility` to `File` and `Dataset` | [307](https://github.com/laminlabs/lnschema-core/pull/307) | [sunnyosun](https://github.com/sunnyosun) | 2023-10-26 | 0.53.0
✨ Enable passing filter expressions to lookup and search | [308](https://github.com/laminlabs/lnschema-core/pull/308) | [sunnyosun](https://github.com/sunnyosun) | 2023-10-25 |
🚚 Remove field email from user | [306](https://github.com/laminlabs/lnschema-core/pull/306) | [falexwolf](https://github.com/falexwolf) | 2023-10-19 | 0.52.0
🚚 Rename `Species` to `Organism` | [305](https://github.com/laminlabs/lnschema-core/pull/305) | [sunnyosun](https://github.com/sunnyosun) | 2023-10-19 |
🚚 Migrate to integer primary keys | [304](https://github.com/laminlabs/lnschema-core/pull/304) | [falexwolf](https://github.com/falexwolf) | 2023-10-13 | 0.51.0
🎨 Add path properties & storage field on Dataset | [303](https://github.com/laminlabs/lnschema-core/pull/303) | [falexwolf](https://github.com/falexwolf) | 2023-10-04 | 0.50.0
🚚 Rename notebook series | [302](https://github.com/laminlabs/lnschema-core/pull/302) | [sunnyosun](https://github.com/sunnyosun) | 2023-10-03 |
✨ Track storage of notebooks | [301](https://github.com/laminlabs/lnschema-core/pull/301) | [falexwolf](https://github.com/falexwolf) | 2023-10-01 | 0.49.0
🎨 Add a `members` property to `FeatureSet` | [300](https://github.com/laminlabs/lnschema-core/pull/300) | [falexwolf](https://github.com/falexwolf) | 2023-09-27 | 0.48.4
📝 Document dataset methods | [299](https://github.com/laminlabs/lnschema-core/pull/299) | [falexwolf](https://github.com/falexwolf) | 2023-09-23 | 0.48.3
✨ Add `reference` and `reference_type` to `Dataset`, `ULabel` | [298](https://github.com/laminlabs/lnschema-core/pull/298) | [sunnyosun](https://github.com/sunnyosun) | 2023-09-15 |
🔥 Remove `add_labels` & `get_labels` & improve documentation of `ULabel` | [297](https://github.com/laminlabs/lnschema-core/pull/297) | [falexwolf](https://github.com/falexwolf) | 2023-09-09 |
🎨 Added return_field to lookup | [296](https://github.com/laminlabs/lnschema-core/pull/296) | [sunnyosun](https://github.com/sunnyosun) | 2023-09-08 |
🚚 Rename `Label` to `ULabel` | [295](https://github.com/laminlabs/lnschema-core/pull/295) | [sunnyosun](https://github.com/sunnyosun) | 2023-09-07 |
🎨 Make field optional for from_values | [293](https://github.com/laminlabs/lnschema-core/pull/293) | [sunnyosun](https://github.com/sunnyosun) | 2023-09-04 |
⬆️ Switch to WRatio and default to limit=20 for search | [292](https://github.com/laminlabs/lnschema-core/pull/292) | [sunnyosun](https://github.com/sunnyosun) | 2023-09-04 | 0.47.4
🚚 Version dataset | [291](https://github.com/laminlabs/lnschema-core/pull/291) | [falexwolf](https://github.com/falexwolf) | 2023-09-02 | 0.47.0
📝 Fix run signature | [289](https://github.com/laminlabs/lnschema-core/pull/289) | [falexwolf](https://github.com/falexwolf) | 2023-09-02 |
📝 Prettify field sorting, improve File & Dataset docstring | [290](https://github.com/laminlabs/lnschema-core/pull/290) | [falexwolf](https://github.com/falexwolf) | 2023-09-02 |
📝 Fix Run docs | [288](https://github.com/laminlabs/lnschema-core/pull/288) | [falexwolf](https://github.com/falexwolf) | 2023-09-01 | 0.46.5
🚚 Add modality to from_df and from_anndata | [285](https://github.com/laminlabs/lnschema-core/pull/285) | [falexwolf](https://github.com/falexwolf) | 2023-08-31 | 0.46.4
♻️ Type features | [287](https://github.com/laminlabs/lnschema-core/pull/287) | [falexwolf](https://github.com/falexwolf) | 2023-08-31 |
🎨 Added include_foregin_keys for _repr_ | [284](https://github.com/laminlabs/lnschema-core/pull/284) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-29 | 0.46.2
📝 Fix docs | [283](https://github.com/laminlabs/lnschema-core/pull/283) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-24 | 0.46.1
🚚 Make suffix non-nullable | [272](https://github.com/laminlabs/lnschema-core/pull/272) | [falexwolf](https://github.com/falexwolf) | 2023-08-23 | 0.46.0
🎨 Make storage root unique | [282](https://github.com/laminlabs/lnschema-core/pull/282) | [falexwolf](https://github.com/falexwolf) | 2023-08-23 |
♻️ Version transform | [279](https://github.com/laminlabs/lnschema-core/pull/279) | [falexwolf](https://github.com/falexwolf) | 2023-08-23 |
🚚 from_anndata and from_df for Dataset | [280](https://github.com/laminlabs/lnschema-core/pull/280) | [falexwolf](https://github.com/falexwolf) | 2023-08-23 |
🚚 Add `modality` to `Feature` | [278](https://github.com/laminlabs/lnschema-core/pull/278) | [falexwolf](https://github.com/falexwolf) | 2023-08-23 |
♻️ Use CanValidate & HasParents | [277](https://github.com/laminlabs/lnschema-core/pull/277) | [falexwolf](https://github.com/falexwolf) | 2023-08-23 |
🚚 Add `transform`, `run` & `input_of` fields to dataset | [276](https://github.com/laminlabs/lnschema-core/pull/276) | [falexwolf](https://github.com/falexwolf) | 2023-08-22 |
🎨 Enable default field for .inspect and .validate | [275](https://github.com/laminlabs/lnschema-core/pull/275) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-22 |
🎨 Merge ValidationAware and SynonymsAware into ValidationMixin | [274](https://github.com/laminlabs/lnschema-core/pull/274) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-22 |
📝 Updated signature of features.from_df | [273](https://github.com/laminlabs/lnschema-core/pull/273) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-18 |
✏️ Fix typo of map_synonyms backward compat | [271](https://github.com/laminlabs/lnschema-core/pull/271) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-17 |
🚚 Rename map_synonyms to standardize | [270](https://github.com/laminlabs/lnschema-core/pull/270) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-16 |
📝 Refactored docs | [269](https://github.com/laminlabs/lnschema-core/pull/269) | [falexwolf](https://github.com/falexwolf) | 2023-08-12 | 0.45.3
💚 Fix import | [268](https://github.com/laminlabs/lnschema-core/pull/268) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-11 | 0.45.2
🚚 Move describe to Data | [267](https://github.com/laminlabs/lnschema-core/pull/267) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-11 | 0.45.1
♻️ Add ParentsAware | [266](https://github.com/laminlabs/lnschema-core/pull/266) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-11 |
🚚 Replace `stem_id` on `File` with `initial_version` | [265](https://github.com/laminlabs/lnschema-core/pull/265) | [falexwolf](https://github.com/falexwolf) | 2023-08-10 | 0.45.0
📝 Updated `validate()` signature | [264](https://github.com/laminlabs/lnschema-core/pull/264) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-08 |
🚚 Add `stem_id` and `version` to `File` | [263](https://github.com/laminlabs/lnschema-core/pull/263) | [falexwolf](https://github.com/falexwolf) | 2023-08-08 |
📝 Remove all duplicated type annotation from docs | [262](https://github.com/laminlabs/lnschema-core/pull/262) | [falexwolf](https://github.com/falexwolf) | 2023-08-08 |
📝 Document all types | [261](https://github.com/laminlabs/lnschema-core/pull/261) | [falexwolf](https://github.com/falexwolf) | 2023-08-08 |
⬆️ Add `InspectResult` | [260](https://github.com/laminlabs/lnschema-core/pull/260) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-07 | 0.44.3
🚸 Turn method `path()` into property `path` | [259](https://github.com/laminlabs/lnschema-core/pull/259) | [falexwolf](https://github.com/falexwolf) | 2023-08-06 | 0.44.2
✨ Added `validate()` | [257](https://github.com/laminlabs/lnschema-core/pull/257) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-06 | 0.44.0
🚚 Rename `ref_field` to `registry` | [256](https://github.com/laminlabs/lnschema-core/pull/256) | [falexwolf](https://github.com/falexwolf) | 2023-08-06 |
♻️ Add `Data` base class for `File` & `Dataset` | [255](https://github.com/laminlabs/lnschema-core/pull/255) | [falexwolf](https://github.com/falexwolf) | 2023-08-05 |
🚚 Rename `ORM` to `Registry` | [254](https://github.com/laminlabs/lnschema-core/pull/254) | [sunnyosun](https://github.com/sunnyosun) | 2023-08-05 |
🚚 Type Link ORMs with `LinkORM` | [253](https://github.com/laminlabs/lnschema-core/pull/253) | [falexwolf](https://github.com/falexwolf) | 2023-08-04 | 0.43.3
🚚 Rename select to filter | [252](https://github.com/laminlabs/lnschema-core/pull/252) | [falexwolf](https://github.com/falexwolf) | 2023-07-31 | 0.43.0
🚚 Rename `Feature.label_orms` to `Feature.registries` | [251](https://github.com/laminlabs/lnschema-core/pull/251) | [falexwolf](https://github.com/falexwolf) | 2023-07-31 |
♻️ Aggregate ref_field, ref_orm, ref_schema into ref_field | [250](https://github.com/laminlabs/lnschema-core/pull/250) | [falexwolf](https://github.com/falexwolf) | 2023-07-31 |
🚚 Move feature foreign key from Label to link model | [249](https://github.com/laminlabs/lnschema-core/pull/249) | [falexwolf](https://github.com/falexwolf) | 2023-07-31 |
🚚 Allow multiple label ORMs in feature | [247](https://github.com/laminlabs/lnschema-core/pull/247) | [falexwolf](https://github.com/falexwolf) | 2023-07-29 |
🚑️ Hash can be null | [246](https://github.com/laminlabs/lnschema-core/pull/246) | [falexwolf](https://github.com/falexwolf) | 2023-07-26 |
📝 Add signatures to remaining ORMs | [245](https://github.com/laminlabs/lnschema-core/pull/245) | [falexwolf](https://github.com/falexwolf) | 2023-07-26 | 0.42.1
🚚 Add field `hash` to `FeatureSet` | [244](https://github.com/laminlabs/lnschema-core/pull/244) | [falexwolf](https://github.com/falexwolf) | 2023-07-26 |
🚸 Type-annotate `FeatureManager` | [243](https://github.com/laminlabs/lnschema-core/pull/243) | [falexwolf](https://github.com/falexwolf) | 2023-07-26 |
🚚 Rename `featureset_id` to `feature_set_id` in `FeatureSetFile` link table | [242](https://github.com/laminlabs/lnschema-core/pull/242) | [falexwolf](https://github.com/falexwolf) | 2023-07-26 |
🚚 Add `Modality` | [240](https://github.com/laminlabs/lnschema-core/pull/240) | [falexwolf](https://github.com/falexwolf) | 2023-07-25 |
🚚 Add `File.accessor` | [239](https://github.com/laminlabs/lnschema-core/pull/239) | [falexwolf](https://github.com/falexwolf) | 2023-07-25 |
🚚 Remove reference Registry from Label and add it to Feature, add slot to FeatureSet link models | [238](https://github.com/laminlabs/lnschema-core/pull/238) | [falexwolf](https://github.com/falexwolf) | 2023-07-24 | 0.41.0
📝 Updated view_parents signature | [237](https://github.com/laminlabs/lnschema-core/pull/237) | [sunnyosun](https://github.com/sunnyosun) | 2023-07-23 | 0.40.1
🚚 More comprehensive `Label` and `FeatureSet` fields | [236](https://github.com/laminlabs/lnschema-core/pull/236) | [falexwolf](https://github.com/falexwolf) | 2023-07-23 |
🚚 Integrate `Category` and `Tag` into `Label` | [235](https://github.com/laminlabs/lnschema-core/pull/235) | [falexwolf](https://github.com/falexwolf) | 2023-07-22 |
🚚 Add `description` and `parents` to `Tag`, delete `Project`, replace `Run.name` with `Run.reference_type`, `Run.inputs` as `File.input_of` | [233](https://github.com/laminlabs/lnschema-core/pull/233) | [falexwolf](https://github.com/falexwolf) | 2023-07-21 |
🚚 Add categories to file and dataset | [232](https://github.com/laminlabs/lnschema-core/pull/232) | [falexwolf](https://github.com/falexwolf) | 2023-07-21 |
💄 Improve docstring | [231](https://github.com/laminlabs/lnschema-core/pull/231) | [sunnyosun](https://github.com/sunnyosun) | 2023-07-20 | 0.39.0
🚚 Rename `FeatureValue` to `Category` | [230](https://github.com/laminlabs/lnschema-core/pull/230) | [falexwolf](https://github.com/falexwolf) | 2023-07-19 |
📝 Add examples to docstring | [229](https://github.com/laminlabs/lnschema-core/pull/229) | [sunnyosun](https://github.com/sunnyosun) | 2023-07-19 |
🚚 Move `feature_sets` to `File` instead of having `files` on `FeatureSet` | [228](https://github.com/laminlabs/lnschema-core/pull/228) | [falexwolf](https://github.com/falexwolf) | 2023-07-19 |
✨ Add `Feature.unit` | [227](https://github.com/laminlabs/lnschema-core/pull/227) | [falexwolf](https://github.com/falexwolf) | 2023-07-19 |
♻️ Refactor `Feature` and add `FeatureValue` | [225](https://github.com/laminlabs/lnschema-core/pull/225) | [falexwolf](https://github.com/falexwolf) | 2023-07-18 |
🔥 Remove top_hit param from search | [226](https://github.com/laminlabs/lnschema-core/pull/226) | [sunnyosun](https://github.com/sunnyosun) | 2023-07-18 |
🍱 Added more methods for signature | [224](https://github.com/laminlabs/lnschema-core/pull/224) | [sunnyosun](https://github.com/sunnyosun) | 2023-07-17 |
🚚 Add `Transform.parents` and `File.hash_type` | [223](https://github.com/laminlabs/lnschema-core/pull/223) | [falexwolf](https://github.com/falexwolf) | 2023-07-07 | 0.38.3
✨ Add `from_df` and `from_anndata` to `File` | [222](https://github.com/laminlabs/lnschema-core/pull/222) | [falexwolf](https://github.com/falexwolf) | 2023-07-05 | 0.38.2
💄 Do not show None fields | [221](https://github.com/laminlabs/lnschema-core/pull/221) | [falexwolf](https://github.com/falexwolf) | 2023-07-03 | 0.38.1
🚚 Move `QuerySet` to lamindb | [220](https://github.com/laminlabs/lnschema-core/pull/220) | [falexwolf](https://github.com/falexwolf) | 2023-07-03 |
✨ Allow for annotate in `.df()` | [219](https://github.com/laminlabs/lnschema-core/pull/219) | [falexwolf](https://github.com/falexwolf) | 2023-07-02 |
🚚 Rename `File.name` to `File.description` | [218](https://github.com/laminlabs/lnschema-core/pull/218) | [falexwolf](https://github.com/falexwolf) | 2023-07-02 | 0.38.0
🚚 Update `Feature` and `FeatureSet` | [217](https://github.com/laminlabs/lnschema-core/pull/217) | [falexwolf](https://github.com/falexwolf) | 2023-07-01 |
💄 Prettify dataframe display | [216](https://github.com/laminlabs/lnschema-core/pull/216) | [falexwolf](https://github.com/falexwolf) | 2023-06-30 |
📝 Fix docs | [215](https://github.com/laminlabs/lnschema-core/pull/215) | [falexwolf](https://github.com/falexwolf) | 2023-06-30 | 0.37.0
🚚 Move `File` docstrings and signatures | [214](https://github.com/laminlabs/lnschema-core/pull/214) | [falexwolf](https://github.com/falexwolf) | 2023-06-29 |
🚚 Rename `BaseORM` to `Registry`, move `Registry` signatures here | [213](https://github.com/laminlabs/lnschema-core/pull/213) | [falexwolf](https://github.com/falexwolf) | 2023-06-29 |
✨ Add `Dataset` & `Feature` ORMs | [212](https://github.com/laminlabs/lnschema-core/pull/212) | [falexwolf](https://github.com/falexwolf) | 2023-06-29 | 0.37a1
💄 Denoise display of timestamps | [211](https://github.com/laminlabs/lnschema-core/pull/211) | [falexwolf](https://github.com/falexwolf) | 2023-06-26 |
🎨 Auto-manage `RunInput` relationship | [210](https://github.com/laminlabs/lnschema-core/pull/210) | [falexwolf](https://github.com/falexwolf) | 2023-06-26 | 0.36.1
🚚 Repurpose `Folder` to `Tag` | [209](https://github.com/laminlabs/lnschema-core/pull/209) | [falexwolf](https://github.com/falexwolf) | 2023-06-22 | 0.36.0
🚚 Move `BaseORM.__init__` to lamindb | [208](https://github.com/laminlabs/lnschema-core/pull/208) | [falexwolf](https://github.com/falexwolf) | 2023-06-19 | 0.35.10
🚚 Expand field length `short_name` in transform | [207](https://github.com/laminlabs/lnschema-core/pull/207) | [falexwolf](https://github.com/falexwolf) | 2023-06-19 |
🔥 Remove `Lookup` | [206](https://github.com/laminlabs/lnschema-core/pull/206) | [sunnyosun](https://github.com/sunnyosun) | 2023-06-15 | 0.35.9
🚚 Move methods to lamindb | [205](https://github.com/laminlabs/lnschema-core/pull/205) | [falexwolf](https://github.com/falexwolf) | 2023-06-15 | 0.35.8
🚚 Make `User.name` nullable | [204](https://github.com/laminlabs/lnschema-core/pull/204) | [falexwolf](https://github.com/falexwolf) | 2023-06-15 |
🔥 Remove unnecessary file | [203](https://github.com/laminlabs/lnschema-core/pull/203) | [falexwolf](https://github.com/falexwolf) | 2023-06-14 |
✅ Add migrations check | [202](https://github.com/laminlabs/lnschema-core/pull/202) | [falexwolf](https://github.com/falexwolf) | 2023-06-14 |
♻️ Alter SA migration strategy | [200](https://github.com/laminlabs/lnschema-core/pull/200) | [falexwolf](https://github.com/falexwolf) | 2023-06-12 | 0.35.7
🍱 Add migration process for legacy SA instances | [199](https://github.com/laminlabs/lnschema-core/pull/199) | [falexwolf](https://github.com/falexwolf) | 2023-06-12 | 0.35.5
♻️ Less customized IDs | [198](https://github.com/laminlabs/lnschema-core/pull/198) | [falexwolf](https://github.com/falexwolf) | 2023-06-12 |
♻️ Move logic to lamindb | [197](https://github.com/laminlabs/lnschema-core/pull/197) | [falexwolf](https://github.com/falexwolf) | 2023-06-12 |
✨ Delete storage in File.delete | [196](https://github.com/laminlabs/lnschema-core/pull/196) | [Koncopd](https://github.com/Koncopd) | 2023-06-12 |
🚚 Rename Featureset to FeatureSet | [194](https://github.com/laminlabs/lnschema-core/pull/194) | [sunnyosun](https://github.com/sunnyosun) | 2023-06-10 | 0.35.4
♻️ Move save logic here | [193](https://github.com/laminlabs/lnschema-core/pull/193) | [falexwolf](https://github.com/falexwolf) | 2023-06-10 | 0.35.3
🔥 Remove unnecessary files | [192](https://github.com/laminlabs/lnschema-core/pull/192) | [falexwolf](https://github.com/falexwolf) | 2023-06-09 | 0.35.2
👷 Simplify CI & remove docs | [191](https://github.com/laminlabs/lnschema-core/pull/191) | [falexwolf](https://github.com/falexwolf) | 2023-06-09 |
🚸 Check for required fields | [190](https://github.com/laminlabs/lnschema-core/pull/190) | [falexwolf](https://github.com/falexwolf) | 2023-06-09 | 0.35.1
🚸 Add select method to `BaseORM` | [189](https://github.com/laminlabs/lnschema-core/pull/189) | [falexwolf](https://github.com/falexwolf) | 2023-06-08 | 0.35.0
🎨 Auto fetch related names for Featureset | [188](https://github.com/laminlabs/lnschema-core/pull/188) | [sunnyosun](https://github.com/sunnyosun) | 2023-06-08 |
🏗️ Re-architect transform id | [186](https://github.com/laminlabs/lnschema-core/pull/186) | [falexwolf](https://github.com/falexwolf) | 2023-06-06 | 0.35a7
🎨 Adapted featureset | [185](https://github.com/laminlabs/lnschema-core/pull/185) | [sunnyosun](https://github.com/sunnyosun) | 2023-06-05 | 0.35a6
♻️ Polish schema | [184](https://github.com/laminlabs/lnschema-core/pull/184) | [falexwolf](https://github.com/falexwolf) | 2023-06-05 |
🚸 Improve QuerySet | [182](https://github.com/laminlabs/lnschema-core/pull/182) | [falexwolf](https://github.com/falexwolf) | 2023-06-05 |
🔥 Delete SQLAlchemy related content | [181](https://github.com/laminlabs/lnschema-core/pull/181) | [falexwolf](https://github.com/falexwolf) | 2023-06-04 |
♻️ Absorb `DjangoORM.create()` in `DjangoORM.__init__()` | [178](https://github.com/laminlabs/lnschema-core/pull/178) | [falexwolf](https://github.com/falexwolf) | 2023-06-03 |
🏗️ Enable Django backend | [177](https://github.com/laminlabs/lnschema-core/pull/177) | [falexwolf](https://github.com/falexwolf) | 2023-06-02 | 0.35a3
🚚 Rename `lndb` to `lamindb-setup` | [176](https://github.com/laminlabs/lnschema-core/pull/176) | [falexwolf](https://github.com/falexwolf) | 2023-06-01 | 0.35a2
🏗️ Add Django backend | [175](https://github.com/laminlabs/lnschema-core/pull/175) | [falexwolf](https://github.com/falexwolf) | 2023-05-31 | 0.35a1
👷 Refactor CI | [174](https://github.com/laminlabs/lnschema-core/pull/174) | [falexwolf](https://github.com/falexwolf) | 2023-05-30 |
🏗️ Remove SQL-level schema modules | [172](https://github.com/laminlabs/lnschema-core/pull/172) | [falexwolf](https://github.com/falexwolf) | 2023-05-25 | 0.34.0
🏗️ Introduce Django skeleton | [171](https://github.com/laminlabs/lnschema-core/pull/171) | [falexwolf](https://github.com/falexwolf) | 2023-05-24 |
♻️ Refactor types | [170](https://github.com/laminlabs/lnschema-core/pull/170) | [falexwolf](https://github.com/falexwolf) | 2023-05-23 |
♻️ Refactor `BaseORM` | [169](https://github.com/laminlabs/lnschema-core/pull/169) | [falexwolf](https://github.com/falexwolf) | 2023-05-17 | 0.33.8
🚸 Add `lazy="joined"` to some cheap joins | [168](https://github.com/laminlabs/lnschema-core/pull/168) | [falexwolf](https://github.com/falexwolf) | 2023-05-16 | 0.33.7
🎨 Replace `data` in `Features` with iterable | [167](https://github.com/laminlabs/lnschema-core/pull/167) | [sunnyosun](https://github.com/sunnyosun) | 2023-05-10 | 0.33.6
🎨 Replace `reference` with `field` in `Features` | [166](https://github.com/laminlabs/lnschema-core/pull/166) | [sunnyosun](https://github.com/sunnyosun) | 2023-05-09 | 0.33.5
✅ Use `nbproject-test` directly | [165](https://github.com/laminlabs/lnschema-core/pull/165) | [Koncopd](https://github.com/Koncopd) | 2023-05-04 |
✨ Enable `.lookup()` | [164](https://github.com/laminlabs/lnschema-core/pull/164) | [sunnyosun](https://github.com/sunnyosun) | 2023-04-24 | 0.33.4
🎨 Refactor `ln.File` | [163](https://github.com/laminlabs/lnschema-core/pull/163) | [falexwolf](https://github.com/falexwolf) | 2023-04-24 | 0.33.3
⚡️ Do not change key for in-memory data replace | [162](https://github.com/laminlabs/lnschema-core/pull/162) | [Koncopd](https://github.com/Koncopd) | 2023-04-23 | 0.33.2
✨ Change File.replace handling of key | [161](https://github.com/laminlabs/lnschema-core/pull/161) | [Koncopd](https://github.com/Koncopd) | 2023-04-23 |
🚚 Move `Folder.subset` to lamindb | [160](https://github.com/laminlabs/lnschema-core/pull/160) | [falexwolf](https://github.com/falexwolf) | 2023-04-22 |
🐛 Fix population of `transform_id` in `File` in edge cases | [159](https://github.com/laminlabs/lnschema-core/pull/159) | [falexwolf](https://github.com/falexwolf) | 2023-04-21 | 0.33.1
🚚 Better names, more relationships directly on `File` | [157](https://github.com/laminlabs/lnschema-core/pull/157) | [falexwolf](https://github.com/falexwolf) | 2023-04-16 | 0.33.0
🐛 Fix `.replace()` for key != None | [156](https://github.com/laminlabs/lnschema-core/pull/156) | [falexwolf](https://github.com/falexwolf) | 2023-04-13 | 0.32.2
🎨 Set `Transform` id upon insert, update `Transform` default | [154](https://github.com/laminlabs/lnschema-core/pull/154) | [falexwolf](https://github.com/falexwolf) | 2023-04-12 | 0.32.1
🚚 Add app type | [155](https://github.com/laminlabs/lnschema-core/pull/155) | [falexwolf](https://github.com/falexwolf) | 2023-04-12 |
🩹 Fix name check in replace | [153](https://github.com/laminlabs/lnschema-core/pull/153) | [Koncopd](https://github.com/Koncopd) | 2023-04-10 |
✨ Overwrite key in replace if needed | [152](https://github.com/laminlabs/lnschema-core/pull/152) | [Koncopd](https://github.com/Koncopd) | 2023-04-10 |
🚸 Use full filename to populate `File.name`, introduce `File.key` and `Folder.key` | [150](https://github.com/laminlabs/lnschema-core/pull/150) | [falexwolf](https://github.com/falexwolf) | 2023-04-08 | 0.32.0
✨ Add `File.replace()` and `File.stage()` | [149](https://github.com/laminlabs/lnschema-core/pull/149) | [Koncopd](https://github.com/Koncopd) | 2023-04-03 | 0.31.0
♻️ Refactor Registry defintions | [148](https://github.com/laminlabs/lnschema-core/pull/148) | [falexwolf](https://github.com/falexwolf) | 2023-03-29 | 0.30.0
🚚 Add `reference` to `Transform` | [147](https://github.com/laminlabs/lnschema-core/pull/147) | [falexwolf](https://github.com/falexwolf) | 2023-03-25 | 0.30rc5
💚 Add weak backward compat | [commit](https://github.com/laminlabs/lnschema-core/commit/aa5ce2c272f0d9f14d7fa36a1298705c8ae6dda2) | [falexwolf](https://github.com/falexwolf) | 2023-03-24 | 0.30rc4
🚚 Rename `DObject` to `File` and `DFolder` to `Folder` | [146](https://github.com/laminlabs/lnschema-core/pull/146) | [falexwolf](https://github.com/falexwolf) | 2023-03-24 | 0.30rc3
🎨 Simplify `Run` | [145](https://github.com/laminlabs/lnschema-core/pull/145) | [falexwolf](https://github.com/falexwolf) | 2023-03-23 |
🏗️ Combine `Notebook` and `Pipeline` into `Transform` | [144](https://github.com/laminlabs/lnschema-core/pull/144) | [falexwolf](https://github.com/falexwolf) | 2023-03-23 | 0.30rc2
🔥 Remove Usage Registry | [143](https://github.com/laminlabs/lnschema-core/pull/143) | [falexwolf](https://github.com/falexwolf) | 2023-03-22 | 0.30rc1
⬆️ typeguard<3.0.0 and update lamindb | [141](https://github.com/laminlabs/lnschema-core/pull/141) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-15 | 0.29.7
🚑 Fix __name__ of reltype | [137](https://github.com/laminlabs/lnschema-core/pull/137) | [falexwolf](https://github.com/falexwolf) | 2023-03-14 | 0.29.6
📝 Fix docs reference | [commit](https://github.com/laminlabs/lnschema-core/commit/e5b7d5d0bc7180e7c145f5ad7eac75db5928fde5) | [falexwolf](https://github.com/falexwolf) | 2023-03-14 | 0.29.5
🚸 Be smart about `global_context` and `load_latest` | [136](https://github.com/laminlabs/lnschema-core/pull/136) | [falexwolf](https://github.com/falexwolf) | 2023-03-14 | 0.29.4
🚚 Rename ref to reference, added backward compat for features_ref | [135](https://github.com/laminlabs/lnschema-core/pull/135) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-14 | 0.29.3
✨ Implement ln.Features | [134](https://github.com/laminlabs/lnschema-core/pull/134) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-14 | 0.29.3rc1
🚚 Move track_run logic here | [133](https://github.com/laminlabs/lnschema-core/pull/133) | [falexwolf](https://github.com/falexwolf) | 2023-03-13 | 0.29.2
🚚 Rename get_object to get | [132](https://github.com/laminlabs/lnschema-core/pull/132) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-01 | 0.29.1
📝 Fix docs references | [130](https://github.com/laminlabs/lnschema-core/pull/130) | [falexwolf](https://github.com/falexwolf) | 2023-02-24 | 0.29.0
📝 Use lamin instead of lndb in guides | [129](https://github.com/laminlabs/lnschema-core/pull/129) | [falexwolf](https://github.com/falexwolf) | 2023-02-24 |
👷 Minimal docs build | [128](https://github.com/laminlabs/lnschema-core/pull/128) | [falexwolf](https://github.com/falexwolf) | 2023-02-24 |
🚸 Change user id back to base62 | [127](https://github.com/laminlabs/lnschema-core/pull/127) | [falexwolf](https://github.com/falexwolf) | 2023-02-24 |
✨ Added `get_dobject` to DFolder | [126](https://github.com/laminlabs/lnschema-core/pull/126) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-24 | 0.28.7
✨ Added unique constraint uq_storage__objectkey_suffix | [125](https://github.com/laminlabs/lnschema-core/pull/125) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-24 |
👷 Use `laminci` | [124](https://github.com/laminlabs/lnschema-core/pull/124) | [falexwolf](https://github.com/falexwolf) | 2023-02-23 |
✨ Create helper functions to add relationships | [121](https://github.com/laminlabs/lnschema-core/pull/121) | [bpenteado](https://github.com/bpenteado) | 2023-02-23 | 0.28.6
✏️ Fixed folderkey typo | [123](https://github.com/laminlabs/lnschema-core/pull/123) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-23 | 0.28.5
🐛 Fixed getting objectkey | [122](https://github.com/laminlabs/lnschema-core/pull/122) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-23 | 0.28.4
🚚 Rename dobjects_features to dobject_features | [120](https://github.com/laminlabs/lnschema-core/pull/120) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-23 | 0.28.3
🚚 Rename _filekey and _folderkey to _objectkey | [119](https://github.com/laminlabs/lnschema-core/pull/119) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-23 | 0.28.2
👷 Upload run outputs to `lamin-site-assets` | [116](https://github.com/laminlabs/lnschema-core/pull/116) | [falexwolf](https://github.com/falexwolf) | 2023-02-22 |
✨ Create DFolder from a folder | [113](https://github.com/laminlabs/lnschema-core/pull/113) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-22 | 0.28.1
🚚 Rename `DObject.run_id` to `DObject.source_id` | [114](https://github.com/laminlabs/lnschema-core/pull/114) | [falexwolf](https://github.com/falexwolf) | 2023-02-21 | 0.28.0
🚑 Fix determination of postgres vs sqlite | [112](https://github.com/laminlabs/lnschema-core/pull/112) | [falexwolf](https://github.com/falexwolf) | 2023-02-17 |
✨ Add relationship between `DFolder` and `DObject` | [110](https://github.com/laminlabs/lnschema-core/pull/110) | [bpenteado](https://github.com/bpenteado) | 2023-02-16 | 0.27.1
🚚 Add column `external_id` to `Run` | [109](https://github.com/laminlabs/lnschema-core/pull/109) | [falexwolf](https://github.com/falexwolf) | 2023-02-14 | 0.27.0
🔧 Ensure all id lengths are multiples of 4 | [108](https://github.com/laminlabs/lnschema-core/pull/108) | [falexwolf](https://github.com/falexwolf) | 2023-02-14 |
🚚 Move `storage` table back to `core` module | [89](https://github.com/laminlabs/lnschema-core/pull/89) | [falexwolf](https://github.com/falexwolf) | 2023-02-14 | 0.26.1
🔥 Remove migration files | [107](https://github.com/laminlabs/lnschema-core/pull/107) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-14 | 0.26.0
⬆️ Upgrade and rename `lndb_setup` to `lndb` (v0.32.0) | [105](https://github.com/laminlabs/lnschema-core/pull/105) | [bpenteado](https://github.com/bpenteado) | 2023-02-13 | 0.25.12
🚚 Rename `track_runin` to `is_run_input` | [104](https://github.com/laminlabs/lnschema-core/pull/104) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-13 | 0.25.11
✨ Added track_runin to DObject.load() | [103](https://github.com/laminlabs/lnschema-core/pull/103) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-13 | 0.25.10
💄 Fix Registry preview message | [102](https://github.com/laminlabs/lnschema-core/pull/102) | [bpenteado](https://github.com/bpenteado) | 2023-02-07 |
🚸 Introduce Registry relationship previews | [101](https://github.com/laminlabs/lnschema-core/pull/101) | [bpenteado](https://github.com/bpenteado) | 2023-02-07 |
🚚 Rename `DSet` to `DFolder` | [100](https://github.com/laminlabs/lnschema-core/pull/100) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-07 | 0.25.9
🔥  Disable Registry relationship preview | [99](https://github.com/laminlabs/lnschema-core/pull/99) | [bpenteado](https://github.com/bpenteado) | 2023-02-02 | 0.25.8
🐛 Fix assigning _cloud_filepath | [98](https://github.com/laminlabs/lnschema-core/pull/98) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-02 | 0.25.7
✨ Added _filekey to DObject for custom file keys | [97](https://github.com/laminlabs/lnschema-core/pull/97) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-02 | 0.25.6
✨ Added _cloud_filepath private attribute | [96](https://github.com/laminlabs/lnschema-core/pull/96) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-02 | 0.25.5
✨ Add rich string representation for Registry classes | [95](https://github.com/laminlabs/lnschema-core/pull/95) | [bpenteado](https://github.com/bpenteado) | 2023-01-31 | 0.25.4
🚸 Auto populate fk constrained fields from `Relationship`s | [94](https://github.com/laminlabs/lnschema-core/pull/94) | [bpenteado](https://github.com/bpenteado) | 2023-01-26 | 0.25.3
🐛 Fix strict type checking for relationships | [93](https://github.com/laminlabs/lnschema-core/pull/93) | [bpenteado](https://github.com/bpenteado) | 2023-01-24 | 0.25.2
🩹 Fix error message in `Relationship` type checking | [92](https://github.com/laminlabs/lnschema-core/pull/92) | [bpenteado](https://github.com/bpenteado) | 2023-01-23 | 0.25.1
✨ Enable data validation with pydantic | [91](https://github.com/laminlabs/lnschema-core/pull/91) | [bpenteado](https://github.com/bpenteado) | 2023-01-20 | 0.25.0
🩹 Fix `_dbconfig` | [90](https://github.com/laminlabs/lnschema-core/pull/90) | [falexwolf](https://github.com/falexwolf) | 2023-01-16 | 0.24.1
👷 Extend CI to py3.8-3.10 | [88](https://github.com/laminlabs/lnschema-core/pull/88) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-12 |
🚚 Add `title` field to `Notebook` | [87](https://github.com/laminlabs/lnschema-core/pull/87) | [falexwolf](https://github.com/falexwolf) | 2023-01-09 | 0.24.0
🔥 Remove backward compat | [86](https://github.com/laminlabs/lnschema-core/pull/86) | [falexwolf](https://github.com/falexwolf) | 2023-01-05 |
👷 Reformat to 176 char line length | [85](https://github.com/laminlabs/lnschema-core/pull/85) | [falexwolf](https://github.com/falexwolf) | 2023-01-05 |
🐛 Fixed bug in DObject not autogenerate id | [84](https://github.com/laminlabs/lnschema-core/pull/84) | [sunnyosun](https://github.com/sunnyosun) | 2022-12-14 | 0.23.2
📝 Update docstring | [83](https://github.com/laminlabs/lnschema-core/pull/83) | [falexwolf](https://github.com/falexwolf) | 2022-12-12 |
🚚 Rename input to inputs | [81](https://github.com/laminlabs/lnschema-core/pull/81) | [falexwolf](https://github.com/falexwolf) | 2022-12-09 | 0.23.1
🐛 Avoid double construction | [80](https://github.com/laminlabs/lnschema-core/pull/80) | [falexwolf](https://github.com/falexwolf) | 2022-12-09 | 0.23.0
🐛 Fix privates | [79](https://github.com/laminlabs/lnschema-core/pull/79) | [falexwolf](https://github.com/falexwolf) | 2022-12-09 | 0.22.4
🐛 Fix size | [78](https://github.com/laminlabs/lnschema-core/pull/78) | [falexwolf](https://github.com/falexwolf) | 2022-12-09 | 0.22.3
✨ Combine `record` with `DObject` | [77](https://github.com/laminlabs/lnschema-core/pull/77) | [sunnyosun](https://github.com/sunnyosun) | 2022-12-09 | 0.22.2
🥅 Fully module-qualified path for `Pipeline` | [75](https://github.com/laminlabs/lnschema-core/pull/75) | [falexwolf](https://github.com/falexwolf) | 2022-12-08 |
💄 Prettify noxfile | [74](https://github.com/laminlabs/lnschema-core/pull/74) | [falexwolf](https://github.com/falexwolf) | 2022-12-08 |
♻️ Clean up migration tests | [73](https://github.com/laminlabs/lnschema-core/pull/73) | [falexwolf](https://github.com/falexwolf) | 2022-12-08 | 0.22.1
✅ Migration testing primitives on postgres | [72](https://github.com/laminlabs/lnschema-core/pull/72) | [falexwolf](https://github.com/falexwolf) | 2022-12-07 |
🚚 Rename `Jupynb` to `Notebook` and add relationships | [69](https://github.com/laminlabs/lnschema-core/pull/69) | [falexwolf](https://github.com/falexwolf) | 2022-12-07 | 0.22.0
🎨 Reorganize, more tests, change `size` to BigInt | [68](https://github.com/laminlabs/lnschema-core/pull/68) | [falexwolf](https://github.com/falexwolf) | 2022-12-07 |
✨ `add_relationship_keys` function | [67](https://github.com/laminlabs/lnschema-core/pull/67) | [falexwolf](https://github.com/falexwolf) | 2022-12-06 |
🐛 Fix import | [66](https://github.com/laminlabs/lnschema-core/pull/66) | [falexwolf](https://github.com/falexwolf) | 2022-12-05 | 0.21.2
✨ Bypass load settings | [65](https://github.com/laminlabs/lnschema-core/pull/65) | [fredericenard](https://github.com/fredericenard) | 2022-12-02 |
🎨 Prettify API & docs | [64](https://github.com/laminlabs/lnschema-core/pull/64) | [falexwolf](https://github.com/falexwolf) | 2022-11-28 |
🍱 Add tested migration | [63](https://github.com/laminlabs/lnschema-core/pull/63) | [falexwolf](https://github.com/falexwolf) | 2022-11-28 | 0.21.1
🚚 Move storage to public | [62](https://github.com/laminlabs/lnschema-core/pull/62) | [fredericenard](https://github.com/fredericenard) | 2022-11-24 | 0.21.0
🚚 Rename `checksum` to `hash` | [60](https://github.com/laminlabs/lnschema-core/pull/60) | [falexwolf](https://github.com/falexwolf) | 2022-11-18 | 0.20.0
🏗️ Add `Features` table | [59](https://github.com/laminlabs/lnschema-core/pull/59) | [falexwolf](https://github.com/falexwolf) | 2022-11-17 | 0.19.0
✨ Add `path` property to `DObject` | [58](https://github.com/laminlabs/lnschema-core/pull/58) | [falexwolf](https://github.com/falexwolf) | 2022-11-14 | 0.18.0
💚 Fix migration | [57](https://github.com/laminlabs/lnschema-core/pull/57) | [falexwolf](https://github.com/falexwolf) | 2022-11-12 | 0.17.1
🏗️ Aggregate `Run` and `DTransform` | [56](https://github.com/laminlabs/lnschema-core/pull/56) | [falexwolf](https://github.com/falexwolf) | 2022-11-11 | 0.17.0
🍱 Add migration for postgres | [55](https://github.com/laminlabs/lnschema-core/pull/55) | [falexwolf](https://github.com/falexwolf) | 2022-11-10 | 0.16.1
🚚 Rename `PipeineRun` to `Run` | [54](https://github.com/laminlabs/lnschema-core/pull/54) | [falexwolf](https://github.com/falexwolf) | 2022-11-10 | 0.16.0
🐛 Fix prefix II | [53](https://github.com/laminlabs/lnschema-core/pull/53) | [falexwolf](https://github.com/falexwolf) | 2022-11-03 | 0.15.2
🐛 Fix prefix | [52](https://github.com/laminlabs/lnschema-core/pull/52) | [falexwolf](https://github.com/falexwolf) | 2022-11-03 | 0.15.1
🎨 Camel case class names | [51](https://github.com/laminlabs/lnschema-core/pull/51) | [falexwolf](https://github.com/falexwolf) | 2022-11-02 | 0.15.0
🍱 Migration and fixes for postgres | [50](https://github.com/laminlabs/lnschema-core/pull/50) | [falexwolf](https://github.com/falexwolf) | 2022-11-02 |
✨ Schema modules on SQL level | [49](https://github.com/laminlabs/lnschema-core/pull/49) | [falexwolf](https://github.com/falexwolf) | 2022-11-01 |
🧑‍💻 Added naming convention | [47](https://github.com/laminlabs/lnschema-core/pull/47) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-20 |
✨ Added `dset` and `project` | [46](https://github.com/laminlabs/lnschema-core/pull/46) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-19 | 0.14.0
🚚 Rename query to select | [45](https://github.com/laminlabs/lnschema-core/pull/45) | [falexwolf](https://github.com/falexwolf) | 2022-10-12 | 0.13.0
🐛 Add migration version | - | [falexwolf](https://github.com/falexwolf) | 2022-10-11 | 0.12.1
✨ Add `checksum` column | [43](https://github.com/laminlabs/lnschema-core/pull/43) | [fredericenard](https://github.com/fredericenard) | 2022-10-11 | 0.12.0
🚚 Add `name` column to user | [42](https://github.com/laminlabs/lnschema-core/pull/42) | [falexwolf](https://github.com/falexwolf) | 2022-10-10 | 0.11.0
🩹 Fix migration script | [41](https://github.com/laminlabs/lnschema-core/pull/41) | [falexwolf](https://github.com/falexwolf) | 2022-10-07 | 0.10.1
🚸 Auto-populated CreatedBy | [40](https://github.com/laminlabs/lnschema-core/pull/40) | [falexwolf](https://github.com/falexwolf) | 2022-10-07 | 0.10.0
🏗️ Remove version column from dobject | [39](https://github.com/laminlabs/lnschema-core/pull/39) | [falexwolf](https://github.com/falexwolf) | 2022-09-30 | 0.9.0
👷 Fix CI setup | [37](https://github.com/laminlabs/lnschema-core/pull/37) | [falexwolf](https://github.com/falexwolf) | 2022-09-26 |
🚸 Fix type annotations of primary keys and add docstrings everywhere  | [35](https://github.com/laminlabs/lnschema-core/pull/35) | [falexwolf](https://github.com/falexwolf) | 2022-09-26 | 0.8.1
✨ Add `size` field to `dobject` | [32](https://github.com/laminlabs/lnschema-core/pull/32) | [falexwolf](https://github.com/falexwolf) | 2022-09-25 | 0.8.0
🍱 Add migration script | [34](https://github.com/laminlabs/lnschema-core/pull/34) | [falexwolf](https://github.com/falexwolf) | 2022-09-24 | 0.7.3
🩹 Fix type annotation of timestamps | [33](https://github.com/laminlabs/lnschema-core/pull/33) | [falexwolf](https://github.com/falexwolf) | 2022-09-24 |
💄 Add noqa to script mako & simpler unique constraint | [31](https://github.com/laminlabs/lnschema-core/pull/31) | [falexwolf](https://github.com/falexwolf) | 2022-09-23 |
✨ Add `insert` to `type.usage` | [30](https://github.com/laminlabs/lnschema-core/pull/30) | [sunnyosun](https://github.com/sunnyosun) | 2022-09-21 |
🚚 Move migrations to package | [29](https://github.com/laminlabs/lnschema-core/pull/29) | [falexwolf](https://github.com/falexwolf) | 2022-09-20 | 0.7.2
🚚 Rename `file_suffix` to `suffix` | [28](https://github.com/laminlabs/lnschema-core/pull/28) | [falexwolf](https://github.com/falexwolf) | 2022-09-18 | 0.7.1
✨ Rename time stamps and make them server default | [27](https://github.com/laminlabs/lnschema-core/pull/27) | [falexwolf](https://github.com/falexwolf) | 2022-09-18 | 0.7.0
🚚 Move testdb into tests dir | [26](https://github.com/laminlabs/lnschema-core/pull/26) | [falexwolf](https://github.com/falexwolf) | 2022-09-18 |
✨ Enable independent migrations across modules | [25](https://github.com/laminlabs/lnschema-core/pull/25) | [falexwolf](https://github.com/falexwolf) | 2022-09-15 | 0.6.0
🩹 Add timestamps to `pipeline` | [24](https://github.com/laminlabs/lnschema-core/pull/24) | [falexwolf](https://github.com/falexwolf) | 2022-08-26 | 0.5.1
🐛 Re-export `pipeline` at root level | [23](https://github.com/laminlabs/lnschema-core/pull/23) | [falexwolf](https://github.com/falexwolf) | 2022-08-26 |
✨ Add table `pipeline` | [22](https://github.com/laminlabs/lnschema-core/pull/22) | [falexwolf](https://github.com/falexwolf) | 2022-08-26 | 0.5.0
♻️ Refactor id, create `type` submodule | [21](https://github.com/laminlabs/lnschema-core/pull/21) | [falexwolf](https://github.com/falexwolf) | 2022-08-24 |
🚸 Change instance & storage id to 10 char, overhaul ID module | [20](https://github.com/laminlabs/lnschema-core/pull/20) | [falexwolf](https://github.com/falexwolf) | 2022-08-24 |
Use id to reference storage | [19](https://github.com/laminlabs/lnschema-core/pull/19) | [fredericenard](https://github.com/fredericenard) | 2022-08-23 | 0.4.1
🚚 Add migration for v0.4.0 | [16](https://github.com/laminlabs/lnschema-core/pull/16) | [falexwolf](https://github.com/falexwolf) | 2022-08-22 | 0.4.0
🏗️ Add indexes and remove `dtransform_out` | [15](https://github.com/laminlabs/lnschema-core/pull/15) | [falexwolf](https://github.com/falexwolf) | 2022-08-22 |
🏗️ Track cloud workspace location | [14](https://github.com/laminlabs/lnschema-core/pull/14) | [fredericenard](https://github.com/fredericenard) | 2022-08-20 | 0.3.3
🚚 Rename package from `lndb-schema-core` to `lnschema-core` | [10](https://github.com/laminlabs/lnschema-core/pull/10) | [falexwolf](https://github.com/falexwolf) | 2022-08-19 | 0.3.2
🗃️ Rename `pipeline` to `pipeline_run` and remove `v` | [9](https://github.com/laminlabs/lnschema-core/pull/9) | [bpenteado](https://github.com/bpenteado) | 2022-08-18 | 0.3.1
🚚 Add migration from v0.1.1 to v0.3.0 | [8](https://github.com/laminlabs/lnschema-core/pull/8) | [falexwolf](https://github.com/falexwolf) | 2022-08-08 |
🚚 Rename `track_do` to `usage` | [6](https://github.com/laminlabs/lnschema-core/pull/6) | [falexwolf](https://github.com/falexwolf) | 2022-08-03 | 0.3.0
🏗️ Attach id `yvzi` and add version table `version_yvzi` | [5](https://github.com/laminlabs/lnschema-core/pull/5) | [falexwolf](https://github.com/falexwolf) | 2022-08-03 |
🗃️ Add `user.handle` | [4](https://github.com/laminlabs/lnschema-core/pull/4) | [falexwolf](https://github.com/falexwolf) | 2022-08-01 | 0.2.1
🏗️ Schema v0.2.0 with `dtransform` | [3](https://github.com/laminlabs/lnschema-core/pull/3) | [falexwolf](https://github.com/falexwolf) | 2022-07-29 | 0.2.0
🚚 Add migrations from `lamindb-schema` | [2](https://github.com/laminlabs/lnschema-core/pull/2) | [falexwolf](https://github.com/falexwolf) | 2022-07-28 |
🚚 Move code from `lamindb-schema` | [1](https://github.com/laminlabs/lnschema-core/pull/1) | [falexwolf](https://github.com/falexwolf) | 2022-07-23 | 0.1.0
