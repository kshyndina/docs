# Sending transactions

Questions about transaction landing, staked validators, and processed-vs-confirmed transaction lifecycle on Solana.

<details>
<summary>My transactions aren't landing successfully. What should I do?</summary>

Triton ensures reliable transaction delivery to the network, but for optimal transaction finalisation, we recommend configuring appropriate priority fees. See our [Priority Fees API](https://kate-6.gitbook.io/triton-one-docs/documentation/sending-transactions/priority-fees-api) for how to set them.

</details>

<details>
<summary>What is the advantage of sending transactions through a staked validator?</summary>

Staked validators have access to a much larger, reserved connection pool for sending transactions. During congestion, that's a significant advantage over the contested public connection pools. We provide stake-weighted QoS routing for free on every Triton subscription -- contact support by clicking the chat icon in the bottom right of your [customer dashboard](https://customers.triton.one) to enable it on your endpoint.

</details>

<details>
<summary>Can a `processed` transaction on Solana still be dropped?</summary>

Yes. A transaction is only final once it reaches `confirmed` or `finalized` commitment. Slots containing `processed` transactions can still be dropped during minority forks or network congestion.

</details>
