import { useConnection, useWallet } from '@solana/wallet-adapter-react';
import { PublicKey, Connection } from '@solana/web3.js';
import * as anchor from "@project-serum/anchor";
import { useEffect, useState } from 'react';


// Replace with your Solana Program ID and the structure of your data account
const PROGRAM_ID = new PublicKey("YourProgramID_1111111111111111111111111111"); 

function SolanaFraudStatusChecker({ transactionId }) {
    const { connection } = useConnection();
    const [fraudStatus, setFraudStatus] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    
    // In a real Anchor app, you would load the IDL here
    // const program = new anchor.Program(idl, PROGRAM_ID, provider);

    useEffect(() => {
        const fetchStatus = async () => {
            if (!transactionId || !connection) return;
            setIsLoading(true);

            try {
                // 1. Derive the PDA (Public Key) where the status is stored, using txId as a seed
                const [statusPDA] = PublicKey.findProgramAddressSync(
                    [Buffer.from(transactionId)], // Use the transaction ID as a seed
                    PROGRAM_ID
                );
                
                // 2. Fetch the data from the PDA account
                // If using Anchor, this would be: program.account.fraudStatus.fetch(statusPDA)
                const accountInfo = await connection.getAccountInfo(statusPDA);

                if (accountInfo) {
                    // 3. Decode the raw data (Simplified: You'd use Anchor's client for this)
                    // Mocking retrieval: assumes the first byte indicates status (0=SAFE, 1=BLOCKED)
                    const statusByte = accountInfo.data[0]; 
                    setFraudStatus(statusByte === 1 ? 'BLOCKED' : 'SAFE');
                } else {
                    setFraudStatus('NOT RECORDED');
                }

            } catch (error) {
                console.error("Error fetching Solana status:", error);
                setFraudStatus('ERROR');
            } finally {
                setIsLoading(false);
            }
        };

        fetchStatus();
    }, [connection, transactionId]);

    if (isLoading) return <p>Checking Solana Ledger...</p>;

    const statusClass = fraudStatus === 'BLOCKED' ? "status-blocked" : "status-safe";

    return (
        <div className={`status-box ${statusClass}`}>
            <h3>On-Chain Verdict (Solana):</h3>
            <p>{fraudStatus}</p>
        </div>
    );
}

