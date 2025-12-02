import { useWallet } from "@solana/wallet-adapter-react";
import { WalletMultiButton } from "@solana/wallet-adapter-react-ui";

function WalletConnectSection() {
    const { publicKey, connected } = useWallet();

    return (
        <div>
            <WalletMultiButton />
            {connected && (
                <p className="status-text">
                    Connected: {publicKey.toBase58().substring(0, 8)}...
                </p>
            )}
        </div>
    );
}

