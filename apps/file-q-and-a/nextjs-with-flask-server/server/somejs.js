const { NodeWallet } = require('@coral-xyz/anchor')
const anchor = require ('@coral-xyz/anchor')
const { PublicKey, Keypair } = require ('@solana/web3.js')
const fs = require('fs')
const wallet = new NodeWallet(
    Keypair.fromSecretKey(
        new Uint8Array(
            JSON.parse(
                fs.readFileSync('/home/st/g3.json').toString()
            )
        )
    )
);
const connection = new Connection("https://rpc.helius.xyz/?api-key=174bd3e2-d17b-492f-902b-710feb5d18bc");

const anchorProvider = new anchor.AnchorProvider(
        connection,
        wallet,
        anchor.AnchorProvider.defaultOptions()
);
const provider = new ClockworkProvider.fromAnchorProvider(anchorProvider);

const cwProgram = new PublicKey("CLoCKyJ6DXBJqqu2VWx9RLbgnwwR6BMHHuyasVmfMzBh")

let accounts = await connection.getProgramAccounts(cwProgram)
for (var acc of accounts.value){

    const threadAccount = await provider.getThreadAccount(acc.pubkey);
    console.log(threadAccount)

}