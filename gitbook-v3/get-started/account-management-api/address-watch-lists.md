# Address watch lists

<mark style="color:red;">This feature is only limited to account management API tokens created with the operator or reseller role.</mark>

### Add watch list

<mark style="color:blue;">`POST /api/v1/subscriptions/:subscription-uuid/address_watch_lists`</mark>

**Parameters**

<table><thead><tr><th width="263.3333333333333">Name</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code>variant</code> <mark style="color:red;">*required</mark></td><td><code>string</code></td><td>Must be either <code>collection</code> or <code>tree</code></td></tr><tr><td><code>encoded_value</code> <mark style="color:red;">*required</mark></td><td><code>string</code></td><td></td></tr></tbody></table>

### List watch lists

<mark style="color:blue;">`GET /api/v1/address_watch_lists`</mark>

**Query parameters**

| Name                | Type     | Description |
| ------------------- | -------- | ----------- |
| `variant`           | `string` |             |
| `subscription_uuid` | `string` |             |
| `subscription_type` | `string` |             |

### Delete watch list

<mark style="color:blue;">`DELETE /api/v1/address_watch_lists/:uuid`</mark>
