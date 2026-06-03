# Auth & headers

### **Auth**

Pass your token in through the Authorization header to make scoped, authenticated requests against the account management API. You can use the `GET /api/v1/accounts` endpoint to test your token. If you get a 200 status code response, your token is being passed correctly. This token is only used for the account management API (`customers.rpcpool.com/api`). You'll create separate tokens for consuming the RPC API.

Examples in this account management API guide are demonstrated using curl, but you should use an HTTP library of your choice.

```
$ curl -H "Authorization: secret" -H "Content-Type: application/json" -H "Accept:application/json" https://customers.triton.one/api/v1/accounts         
```

### **Headers**

All endpoints accept and return JSON, and you should pass both an Accept and Content-Type header of `application/json`
