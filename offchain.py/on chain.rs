pub mod sentinel_ledger {
    use super::*;

    /// 1. ORACLE CONSUMER FUNCTION: Receives and processes the AI Fraud Score.
    /// This function is called by the trusted Oracle account.
    pub fn record_fraud_score(
        ctx: Context<RecordFraudScore>,
        transaction_id: [u8; 32],
        fraud_score_percent: u8, // Score from 0 to 100
    ) -> Result<()> {
        
        let fraud_record = &mut ctx.accounts.fraud_record;
        
        // --- 1. ORACLE AUTHENTICATION ---
        // (Placeholder: In a production setup, you would verify that 
        // ctx.accounts.oracle_signer is the specific, trusted Oracle address.)
        // require!(ctx.accounts.oracle_signer.key() == *ORACLE_PUBKEY, CustomError::InvalidOracle);

        // --- 2. FRAUD LEDGER LOGIC ---
        
        // Define the threshold for blocking (e.g., 80%)
        const BLOCK_THRESHOLD: u8 = 80;

        fraud_record.transaction_id = transaction_id;
        fraud_record.fraud_score = fraud_score_percent;
        fraud_record.timestamp = Clock::get()?.unix_timestamp;

        // Apply automatic enforcement based on the score
        if fraud_score_percent >= BLOCK_THRESHOLD {
            fraud_record.action_taken = FraudAction::Blocked;
        } else {
            fraud_record.action_taken = FraudAction::Approved;
        }

        msg!("Recorded Transaction: {:?}", transaction_id);
        msg!("Fraud Score: {}%", fraud_record.fraud_score);
        msg!("Action: {:?}", fraud_record.action_taken);

        Ok(())
    }
}

// --- Contexts (Data Structures for Instruction Accounts) ---

/// Defines the accounts required for the 'record_fraud_score' instruction.
#[derive(Accounts)]
#[instruction(transaction_id: [u8; 32])]
pub struct RecordFraudScore<'info> {
    /// CHECK: The Oracle Signer (trusted key that calls this instruction)
    /// Used for authentication (must be checked in the instruction logic)
    pub oracle_signer: Signer<'info>,

    /// PDA (Program Derived Address) that serves as the FRAUD LEDGER record.
    /// It is deterministically created using seeds (the transaction ID).
    #[account(
        init, // Initialize the account (create it)
        payer = oracle_signer, // The Oracle pays the rent for the account
        space = FraudRecord::LEN, // Allocate space for the data structure
        seeds = [b"fraud", transaction_id.as_ref()], // Seeds to derive the address
        bump
    )]
    pub fraud_record: Account<'info, FraudRecord>,

    /// The System Program is always required for creating accounts
    pub system_program: Program<'info, System>,
    
    // The Clock Sysvar is needed to record the timestamp
    // pub clock: Sysvar<'info, Clock>, // Already accessed via Clock::get()? 
}

// --- Data Structures (The Immutable Fraud Ledger) ---

/// The structure that holds the immutable fraud record data.
#[account]
pub struct FraudRecord {
    pub transaction_id: [u8; 32], // Unique ID for the transaction being checked
    pub fraud_score: u8,         // AI score (0-100%)
    pub action_taken: FraudAction, // The automated decision (Blocked/Approved)
    pub timestamp: i64,          // Time of record (for auditability)
    pub bump: u8,                // PDA bump seed
}

// Implement a constant for the account space required (for Anchor's init macro)
impl FraudRecord {
    pub const LEN: usize = 8 // Anchor discriminator
        + 32 // transaction_id
        + 1  // fraud_score
        + 1  // action_taken (enum size)
        + 8  // timestamp
        + 1  // bump
        + 100; // Buffer for future expansion/safety (adjust as needed)
}

/// Enum for the automated action taken by the contract
#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy, PartialEq, Debug)]
pub enum FraudAction {
    Approved,
    Flagged,
    Blocked,
}

// --- Custom Error Handling ---

#[error_code]
pub enum CustomError {
    #[msg("The signer is not the authorized Oracle.")]
    InvalidOracle,
}