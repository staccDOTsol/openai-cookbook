const { NodeWallet } = require('@project-serum/common')
const anchor = require ('@coral-xyz/anchor')
const { PublicKey, Keypair, Connection, Transaction } = require ('@solana/web3.js')
const fs = require('fs')
const { ClockworkProvider } = require('./sdk/lib')
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
const clockworkProvider = new ClockworkProvider(wallet, connection);

const cwProgram = new PublicKey("3XXuUFfweXBwFgFfYaejLvZE4cGZiHgKiGfMtdxNzYmv")
setTimeout(async function (){
let accounts = await connection.getProgramAccounts(cwProgram)
console.log(accounts)
for (var acc of accounts){
try {
        let del = await clockworkProvider.threadDelete(wallet.publicKey, acc.pubkey)
        console.log(del)
        let tx = new Transaction()
        del.programId = new PublicKey("3XXuUFfweXBwFgFfYaejLvZE4cGZiHgKiGfMtdxNzYmv")
        tx.add(del)
        tx.feePayer = wallet.publicKey 
        tx.recentBlockhash = (await connection.getLatestBlockhash()).blockhash
        try {
         anchorProvider.sendAndConfirm(tx)
        } catch (err){
            console.log(err)
        }
} 
 catch (err){
    console.log(err)
 }
}
})