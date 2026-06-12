# Rate limits

### **Overview**

A rate limit caps how many requests per second an endpoint accepts. Triton enforces it per IP across all nodes to keep endpoints stable and protect against abusive traffic&#x20;

Our goal is to allow legitimate application traffic to flow smoothly while mitigating the impact of aggressive bots.

Endpoints authenticated with a token get a more favourable rate limit than endpoints restricted by allowed origins, since tokens are typically used by backend servers (many users per IP) and allowed origins by browsers (one user per IP).

Rate limits do not affect pricing. Our products are billed by usage (per million requests plus per GB of bandwidth).

### **Get rate limits**

<mark style="color:red;">This API is only limited to account management API tokens created with the reseller role.</mark>

<mark style="color:blue;">`GET /api/v1/rate_tiers`</mark>

Returns all Rate Tier types that an Endpoint and Token can get created with.

```json
{
  "rate_tiers": [
    { "name": "free" },
    { "name": "tier1" },
    { "name": "tier2" },
    { "name": "tier3" },
    { "name": "dedi" }
  ]
} 
```
