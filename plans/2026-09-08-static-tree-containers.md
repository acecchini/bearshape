# Give ordinary Tree consumers a useful static type

Owner update (2026-09-08): the reviewed implementation and recorded validation
are approved for merge. This supersedes earlier pending-approval statements.
Full native union composition remains required through supported upstream
integration, with a later candidate allowed; limited CuPy native static support
is accepted. Current merge execution and remaining release gates are tracked in
`plans/2026-09-08-agent-workflow.md` and the production-readiness roadmap.



Maintain this ExecPlan according to `PLANS.md`. This independent PR addresses the Tree portion of audit A06 and is stacked on checker harness PR #17. Runtime tree traversal and structure binding remain unchanged.

## Purpose / Big Picture


Tree[int] should accept integer leaves and existing typed lists, tuples and dictionaries of integer leaves. It should reject strings and wrong nested leaves. The present nominal stub rejects real containers. Replace it only after demonstrating a model that retains leaf information in all four supported checkers.

## Progress


- [x] (2026-09-08) Created feature worktree and tested recursive-container/protocol prototypes with all four checkers.
- [x] (2026-09-08) Opened PR #20 and reproduced real-call failures with the old nominal stubs.
- [x] (2026-09-08) Replaced both nominal stubs with one shared static model under TYPE_CHECKING.
- [x] (2026-09-08) Verified ordinary pretyped containers, named tuples, arrays, empty inputs, strings, fourteen negative sites per checker, and the concrete custom JAX node alias.
- [x] (2026-09-08) All four engines pass on Python 3.10–3.14 and floor lanes. Exact rc0 endpoints each pass 108 tree tests. Locked dev tox: 1,044 passed, five expected skips, 91.24% coverage.
- [x] (2026-09-08) Updated docs/changelog and recorded default-registry limits. Hooks pass.

## Surprises & Discoveries


A recursive alias using list/dict directly rejects already-typed containers because their element types are invariant. In the same prototype ty accepts even deliberate errors. A sequence/protocol model can admit strings through recursive iteration: type stubs expose inherited sequence behavior that is not equivalent to Python's runtime attributes. Another protocol version rejects direct strings but mypy accepts a list of strings.

The current successful small probe uses private covariant protocols for list, tuple and mapping behavior, with a nonrecursive outer union. List's pop result carries recursive leaf information; tuple indexing and tuple concatenation distinguish it from self-iterating strings; mapping values carry recursive leaf information without constraining keys. All four engines accept six valid pretyped cases and reject both deliberate wrong cases. These protocol members are descriptive only; validation does not call them or mutate inputs. The full implementation must extend the probe to mixed nesting, NumPy leaves and additional invalid forms before promotion.

## Decision Log


Decision: Preserve Tree[Leaf] syntax and share the model in the TYPE_CHECKING section of `src/bearshape/_tree.py`, re-exporting it from optree/JAX. Rationale: the two public tree backends should not carry divergent fake nominal classes or duplicate static definitions. No runtime dependency or new module is needed. The existing typing_extensions.TypeAliasType represents the outer alias so ty also retains existing checker-only aliases built from Tree. Date: 2026-09-08.

Decision: Establish tested static support for ordinary lists, tuples, dictionaries, leaves and None; keep arbitrary backend registration a runtime property. Rationale: Python static typing cannot infer a dynamically modified pytree registry. For custom nodes, document the existing TYPE_CHECKING alias pattern using the user's concrete node type and the runtime Tree annotation. This preserves existing runtime support without introducing a new public form or claiming every structural match is registered.

## Outcomes & Retrospective


Implemented real ordinary-container acceptance and maintained exact negative diagnostics for direct/nested strings and invalid array dtypes. The same positive consumer executes with beartype, including a custom registered JAX node; a separate runtime test rejects that node with the wrong leaf dtype. State backend registration limits accurately. Structure-bearing Tree syntax remains runtime-only.

## Context and Orientation


Worktree `/Users/ale/Code/bearshape-worktrees/static-tree-containers`, branch `codex/static-tree-containers`, base `3eac024`. `src/bearshape/_tree.py` owns runtime traversal and structure checking. The TYPE_CHECKING branches in `optree.py` and `jax.py` each define a nominal Tree class. `tests/typing/` and `tests/typing_negative/` use the four-engine harness from PR #17. `tests/test_tree.py` owns runtime tree regressions; add an executable consumer fixture and a maintained runtime invocation there.

## Plan of Work


Add real positive consumer calls with typed leaves, list[int], list[list[int]], tuple mixtures, dict[str, list[int]], None, empty containers, and nested NumPy arrays. Add negative wrong scalars, nested strings, sets and incompatible NumPy dtype examples for both optree/JAX aliases. Save the failing-before checker results.

Implement private covariant protocols and the shared static Tree alias under TYPE_CHECKING in `_tree.py`; replace the public nominal classes with imports of that alias. Use the smallest protocol member sets demonstrated by the prototypes. Extend inference checks to ensure a Tree annotation does not collapse to Any/Unknown. Execute positive consumer functions decorated with beartype so the same examples establish runtime acceptance. Keep custom-node registration and structure binding unchanged and covered by existing tests.

Document the ordinary-container model, the runtime registry boundary and the existing conditional-alias technique for custom registered node types. Do not imply that a structurally matching arbitrary class is registered automatically. Update CHANGELOG. Repeat the complete checker contract on Python 3.10–3.14 and maintained floor engines; run runtime tree tests with exact rc0 endpoints, hooks and locked dev coverage.

## Concrete Steps


From this worktree:

    uv sync --locked
    uv run --locked pytest tests/test_typecheck.py -n 4
    uv run --locked pytest tests/test_tree.py -n 4
    uv run --locked tox run -e dev
    uv run --locked prek run -a

Before implementation preserve the nominal-stub failures. Use interpreter-matched environments for the other Python versions and the existing exact-rc0 CPU environments for runtime source checks. The integrated artifact milestone must repeat consumer checking against the installed wheel.

## Validation and Acceptance


Every checker accepts the maintained valid pretyped containers and rejects all marked errors at the intended source line/category. None and empty containers match actual backend flattening. NumPy leaf annotations retain useful dtype information. Runtime-decorated consumers and existing tree tests pass; no runtime mutation, registry change, Any-valued leaf, or broad new checker suppression is introduced. Custom nodes retain their existing runtime path and have an explicit static spelling based on the user's concrete node type.

## Idempotence and Recovery


Keep prototypes outside the source package and preserve their counterexamples. Only promote the model after complete negative/inference proof. Work remains isolated from other PRs until integration. Do not merge without user validation.

## Artifacts and Notes


Prototypes are under `/Users/ale/Code/bearshape-implementation-2026-09-08/evidence/tree-typing-prototypes/`: `recursive_containers.py`, `recursive_protocols.py`, `reverse_protocols.py`, and `pop_protocols.py`, with per-engine outputs. The first three demonstrate why acceptance-only validation is inadequate. Production evidence uses `tree-typing-*.log`: `before` captures the nominal-stub failures; `focused` captures the initial 115 passing tree/checker tests; `tox` captures 1,044 passing dev tests, 91.24% coverage and all floor engines; `python-3.11` through `python-3.14` capture the interpreter-matched checker matrix; `rc0-py310` and `rc0-py314` each report 108 passing tree tests; `hooks-final` is clean. The final model uses tuple indexing because pinned pyrefly describes named-tuple iteration as Iterable rather than Iterator. A namespaced optree custom registration is not visible to the current default-registry Tree; the maintained custom-node example is explicitly JAX.

## Interfaces and Dependencies


Keep public `bearshape.optree.Tree` and `bearshape.jax.Tree` subscriptions unchanged. The static alias describes leaves and supported container behavior; runtime still uses _TreeFactory and the backend registry. Use standard typing/collections protocols and the existing checker harness. No new runtime or development dependency is required.

Revision note — 2026-09-08: Recorded prototype counterexamples and focused Tree implementation plan before source changes.

Revision note — 2026-09-08: Implemented and validated the shared static model, corrected the prototype for named tuples and existing aliases, and documented the actual registry boundary.

Revision note (2026-09-08): reconciled completed milestone/hosted evidence and
explicit owner merge approval. The combined artifact, checker and GPU proofs
are in `docs/maintainers/production-readiness.md`; this update does not mark
the unresolved native-union integration or release administration complete.
