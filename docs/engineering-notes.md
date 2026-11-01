# Engineering investigation notes

This page documents investigations and engineering lessons separately from the [merged upstream contributions](../README.md#merged-upstream-engineering). **An investigation is not a merged contribution.**

## DJV Information-panel search and pull-request test discovery

- **Contribution:** [DJV PR #919](https://github.com/grizzlypeak3d/DJV/pull/919), authored by BackendArchitectX.
- **Status:** Closed without merging. The earlier [PR #918](https://github.com/grizzlypeak3d/DJV/pull/918) was superseded by the proposed work in #919.
- **Related request:** [DJV issue #316](https://github.com/grizzlypeak3d/DJV/issues/316).

### Engineering problem

The Information panel needed clear multiword-search behavior. The PR also investigated a CI issue: a pull-request build could invoke CTest after building a configuration without tests, creating a misleading successful check when no tests were discovered.

### Investigation and proposed approach

The PR explored a provisional implied-AND interpretation for search, row matching across labels and values, and regression tests. It also proposed building the tested `ci-linux` configuration and treating empty test discovery as a failure, rather than accepting a zero-test run.

The search semantics were **not settled** in that proposal. In particular, the proposed implied-AND behavior should not be described as the upstream behavior.

### Upstream outcome and attribution

The maintainer independently authored and committed the changes that went upstream:

- [Search change — 2e67a24](https://github.com/grizzlypeak3d/DJV/commit/2e67a2401d2704ac7005f8c4685c3f1d9f2c7a5b): matching is by **any** search word against a row's name or value, rather than the proposed implied-AND behavior.
- [CI configuration change — d249d10](https://github.com/grizzlypeak3d/DJV/commit/d249d10cb9832779cc8e3ea30e5cf8fca3c77bdb): the PR check builds the `ci-linux` test-enabled configuration instead of the default configuration that had no tests.

**My PR #919 was not merged.** These maintainer commits are linked to acknowledge the resolution and are not claimed as my authored or merged code.

### Reusable lessons

1. Agree on search semantics before implementing behavioral changes; different interpretations can produce materially different UI results.
2. A green CI job is not proof of regression coverage if it can discover zero tests.
3. Keep test discovery and executed test counts visible, and use test-enabled configurations for PR validation.
4. Distinguish a documented investigation from a maintainer-authored upstream fix.

*Reviewed against upstream PR and commit records on November 2, 2026.*
