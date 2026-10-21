# jobject releases

## 1.0.5
- Added `to_dict()` method to allow reverting back to `dict`.
- Added several overrides of `dict` methods to gaurantee all jobjects contain
`jobject` children and don't accidently have `dict` values.

## 1.0.4
- Allowed `import jobject` alongside `from jobject import jobject`.
- Removed deprecated `JObject`

## 1.0.3
- Added `__delattr__` so variables can be deleted via dot notation.

## 1.0.2
- Fixed an error message in jobject.\_\_getattr\_\_.

## 1.0.1
- Renamed JObject to jobject but left an alias to JObject with a deprecation
warning.

## 1.0.0
- Initial release.