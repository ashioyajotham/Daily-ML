from abc import ABC


class BankingSystem(ABC):
    """
    `BankingSystem` interface.
    """

    def create_account(self, timestamp: int, account_id: str) -> bool:
        """
        Should create a new account with the given identifier if it
        does not already exist.
        Returns `True` if the account was successfully created or
        `False` if an account with `account_id` already exists.
        """
        # default implementation
        return False

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        """
        Should deposit the given `amount` of money to the specified
        `account_id`.
        Returns the total amount of money in the account after the
        query has been processed.
        If the specified account does not exist, should return
        `None`.
        """
        # default implementation
        return None

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        """
        Should transfer the given amount of money from account
        `source_account_id` to account `target_account_id`.
        Returns the balance of `source_account_id` if the transfer
        was successful or `None` otherwise.
          * Returns `None` if `source_account_id` or
          `target_account_id` doesn't exist.
          * Returns `None` if `source_account_id` and
          `target_account_id` are the same.
          * Returns `None` if account `source_account_id` has
          insufficient funds to perform the transfer.
        """
        # default implementation
        return None
        
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        """
        Should return identifiers of the top n accounts with the highest amount
        of outgoing transactions.
        
        Returns a list of strings in the format:
        ["<account_id_1>(<total_outgoing_1>)", "<account_id_2>(<total_outgoing_2>)", ...]
        
        Accounts are sorted by:
        1. Descending order of outgoing transaction amounts
        2. In case of a tie, alphabetically by account_id in ascending order
        
        If less than n accounts exist, returns all account identifiers in the described format.
        """
        # default implementation
        return []
        
    def schedule_payment(self, timestamp: int, account_id: str, amount: int, delay: int) -> str | None:
        """
        Should schedule a payment which will be performed at timestamp + delay.
        Returns a string with a unique identifier for the scheduled payment in the format:
        "payment[ordinal number of the scheduled payment across all accounts]" - e.g., "payment1", "payment2", etc.
        
        If account_id doesn't exist, should return None.
        The payment is skipped if the specified account has insufficient funds when the payment is performed.
        """
        # default implementation
        return None
    
    def cancel_payment(self, timestamp: int, account_id: str, payment_id: str) -> bool:
        """
        Should cancel the scheduled payment with payment_id.
        Returns True if the scheduled payment is successfully canceled.
        
        Returns False if payment_id does not exist or was already canceled,
        or if account_id is different from the source account for the scheduled payment.
        
        Note that scheduled payments must be performed before any cancel_payment operations
        at the given timestamp.
        """
        # default implementation
        return False
        
    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        """
        Should merge account_id_2 into account_id_1.
        Returns True if accounts were merged successfully, or False otherwise.
        
        Returns False if account_id_1 is equal to account_id_2.
        Returns False if either account_id_1 or account_id_2 doesn't exist.
        
        The balance of account_id_2 should be added to the balance of account_id_1.
        All existing scheduled payments for account_id_2 should be scheduled for account_id_1.
        After the merge, it must be possible to cancel any existing scheduled payments for 
        account_id_2 by replacing account_id_2 with account_id_1.
        account_id_2 should be removed from the system after the merge.
        """
        # default implementation
        return False
        
    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        """
        Should return the total amount of money in the account account_id at the given timestamp time_at.
        If the specified account did not exist at time_at, should return None.
        
        If queries have been processed at timestamp time_at, get_balance must reflect the
        account balance after the query has been processed.
        
        If the account was merged into another account, the merged account should inherit
        its balance history.
        """
        # default implementation
        return None


class BankingSystemImpl(BankingSystem):
    def __init__(self):
        # Dictionary to store accounts and their balances
        self.accounts = {}
        # Dictionary to track outgoing transactions for each account
        self.outgoing_transactions = {}
        # Dictionary to store scheduled payments
        self.scheduled_payments = {}
        # Counter for generating unique payment IDs
        self.payment_counter = 0
        # Track canceled payments
        self.canceled_payments = set()
        # Track the last processed timestamp
        self.last_processed_timestamp = -1
        # Track balance history for accounts
        self.balance_history = {}
        # Track merged accounts (old_account -> new_account)
        self.merged_accounts = {}
        # Track operation history
        self.operations = {}
        # Track deleted accounts
        self.deleted_accounts = set()

    def create_account(self, timestamp: int, account_id: str) -> bool:
        """
        Creates a new account with the given identifier if it does not already exist.
        
        Args:
            timestamp (int): A unique timestamp in milliseconds.
            account_id (str): The identifier for the account.
            
        Returns:
            bool: True if the account was successfully created, False if the account already exists.
        """
        # Process any scheduled payments first
        self._process_scheduled_payments(timestamp)
        
        # Check if account already exists or was deleted after a merge
        if account_id in self.accounts or account_id in self.deleted_accounts:
            return False
        
        # Create a new account with zero balance
        self.accounts[account_id] = 0
        # Initialize outgoing transactions tracking for this account
        self.outgoing_transactions[account_id] = 0
        # Initialize balance history
        self.balance_history[account_id] = [(timestamp, 0)]
        # Record this operation
        self.operations[timestamp] = ("create_account", account_id)
        
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        """
        Deposits the given amount of money to the specified account.
        
        Args:
            timestamp (int): A unique timestamp in milliseconds.
            account_id (str): The identifier for the account.
            amount (int): The amount to deposit.
            
        Returns:
            int | None: The total amount of money in the account after the query has been processed,
                        or None if the specified account does not exist.
        """
        # First process any scheduled payments at this timestamp
        self._process_scheduled_payments(timestamp)
        
        # Check if account was deleted (after merging)
        if account_id in self.deleted_accounts:
            return None
            
        # Check if account was merged
        account_id = self._get_current_account_id(account_id)
        
        if account_id not in self.accounts:
            return None
        
        # Add amount to the account balance
        self.accounts[account_id] += amount
        
        # Update balance history
        self.balance_history[account_id].append((timestamp, self.accounts[account_id]))
        
        # Record this operation
        self.operations[timestamp] = ("deposit", account_id, amount)
        
        return self.accounts[account_id]

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        """
        Transfers the given amount of money from the source account to the target account.
        
        Args:
            timestamp (int): A unique timestamp in milliseconds.
            source_account_id (str): The identifier for the source account.
            target_account_id (str): The identifier for the target account.
            amount (int): The amount to transfer.
            
        Returns:
            int | None: The balance of the source account if the transfer was successful, or None otherwise.
        """
        # First process any scheduled payments at this timestamp
        self._process_scheduled_payments(timestamp)
        
        # Check if accounts were deleted (after merging)
        if source_account_id in self.deleted_accounts or target_account_id in self.deleted_accounts:
            return None
        
        # Check if accounts were merged
        source_account_id = self._get_current_account_id(source_account_id)
        target_account_id = self._get_current_account_id(target_account_id)
        
        # Check if both accounts exist
        if source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None
        
        # Check if source and target accounts are the same
        if source_account_id == target_account_id:
            return None
        
        # Check if source account has sufficient funds
        if self.accounts[source_account_id] < amount:
            return None
        
        # Transfer money
        self.accounts[source_account_id] -= amount
        self.accounts[target_account_id] += amount
        
        # Track the outgoing transaction for the source account
        self.outgoing_transactions[source_account_id] += amount
        
        # Update balance history for both accounts
        self.balance_history[source_account_id].append((timestamp, self.accounts[source_account_id]))
        self.balance_history[target_account_id].append((timestamp, self.accounts[target_account_id]))
        
        # Record this operation
        self.operations[timestamp] = ("transfer", source_account_id, target_account_id, amount)
        
        return self.accounts[source_account_id]
        
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        """
        Returns identifiers of the top n accounts with the highest amount of outgoing transactions.
        
        Args:
            timestamp (int): A unique timestamp in milliseconds.
            n (int): The number of top spenders to return.
            
        Returns:
            list[str]: A list of account identifiers in the format 
                      ["account_id(total_outgoing)", ...] sorted by outgoing transactions
                      in descending order. In case of a tie, sorted alphabetically.
        """
        # First process any scheduled payments at this timestamp
        self._process_scheduled_payments(timestamp)
        
        # Create a list of tuples (account_id, outgoing_amount)
        spender_data = [(account_id, amount) for account_id, amount in self.outgoing_transactions.items()
                        if account_id in self.accounts]  # Only include accounts that still exist
        
        # Sort the list:
        # 1. First by outgoing transaction amount in descending order
        # 2. Then by account_id alphabetically in ascending order in case of a tie
        sorted_spenders = sorted(spender_data, key=lambda x: (-x[1], x[0]))
        
        # Limit to the top n spenders (or all if fewer than n accounts exist)
        top_n = sorted_spenders[:n]
        
        # Format the output as required: ["account_id(outgoing_amount)", ...]
        result = [f"{account_id}({amount})" for account_id, amount in top_n]
        
        return result
    
    def schedule_payment(self, timestamp: int, account_id: str, amount: int, delay: int) -> str | None:
        """
        Schedules a payment which will be performed at timestamp + delay.
        
        Args:
            timestamp (int): A unique timestamp in milliseconds.
            account_id (str): The identifier for the account.
            amount (int): The amount of the payment.
            delay (int): The delay in milliseconds after which the payment should be executed.
            
        Returns:
            str | None: A unique identifier for the scheduled payment or None if the account doesn't exist.
        """
        # First process any scheduled payments at this timestamp
        self._process_scheduled_payments(timestamp)
        
        # Check if account was deleted (after merging)
        if account_id in self.deleted_accounts:
            return None
            
        # Check if account was merged
        account_id = self._get_current_account_id(account_id)
        
        # Check if the account exists
        if account_id not in self.accounts:
            return None
        
        # Generate a unique payment ID
        self.payment_counter += 1
        payment_id = f"payment{self.payment_counter}"
        
        # Schedule the payment
        execution_time = timestamp + delay
        self.scheduled_payments[payment_id] = {
            "account_id": account_id,
            "amount": amount,
            "execution_time": execution_time,
            "created_at": timestamp
        }
        
        # Record this operation
        self.operations[timestamp] = ("schedule_payment", account_id, amount, delay, payment_id)
        
        return payment_id
    
    def cancel_payment(self, timestamp: int, account_id: str, payment_id: str) -> bool:
        """
        Cancels a scheduled payment.
        
        Args:
            timestamp (int): A unique timestamp in milliseconds.
            account_id (str): The identifier for the account.
            payment_id (str): The identifier of the payment to cancel.
            
        Returns:
            bool: True if the payment was successfully canceled, False otherwise.
        """
        # First process any scheduled payments at this timestamp
        self._process_scheduled_payments(timestamp)
        
        # Check if account was deleted (after merging)
        if account_id in self.deleted_accounts:
            return False
            
        # Check if account was merged
        account_id = self._get_current_account_id(account_id)
        
        # Check if payment exists and hasn't been canceled yet
        if payment_id not in self.scheduled_payments:
            return False
        
        # Check if payment has already been canceled
        if payment_id in self.canceled_payments:
            return False
        
        # Check if the payment belongs to the specified account
        if self.scheduled_payments[payment_id]["account_id"] != account_id:
            return False
        
        # Check if the payment execution time is in the future
        if self.scheduled_payments[payment_id]["execution_time"] <= timestamp:
            return False
        
        # Mark the payment as canceled
        self.canceled_payments.add(payment_id)
        
        # Record this operation
        self.operations[timestamp] = ("cancel_payment", account_id, payment_id)
        
        return True
    
    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        """
        Merges account_id_2 into account_id_1.
        
        Args:
            timestamp (int): A unique timestamp in milliseconds.
            account_id_1 (str): The target account for the merge.
            account_id_2 (str): The source account that will be merged and removed.
            
        Returns:
            bool: True if the accounts were successfully merged, False otherwise.
        """
        # First process any scheduled payments at this timestamp
        self._process_scheduled_payments(timestamp)
        
        # Check if accounts are the same
        if account_id_1 == account_id_2:
            return False
            
        # Check if either account has been deleted (after a merge)
        if account_id_1 in self.deleted_accounts or account_id_2 in self.deleted_accounts:
            return False
        
        # Get current account IDs in case they were merged
        current_account_id_1 = self._get_current_account_id(account_id_1)
        current_account_id_2 = self._get_current_account_id(account_id_2)
        
        # Check if both accounts exist
        if current_account_id_1 not in self.accounts or current_account_id_2 not in self.accounts:
            return False
        
        # Merge balances
        self.accounts[current_account_id_1] += self.accounts[current_account_id_2]
        
        # Merge outgoing transactions
        self.outgoing_transactions[current_account_id_1] += self.outgoing_transactions[current_account_id_2]
        
        # Update scheduled payments from account_id_2 to account_id_1
        for payment_id, payment_data in self.scheduled_payments.items():
            if payment_data["account_id"] == current_account_id_2 and payment_id not in self.canceled_payments:
                self.scheduled_payments[payment_id]["account_id"] = current_account_id_1
        
        # Update balance history
        # Add current balance to account_id_1 history
        self.balance_history[current_account_id_1].append((timestamp, self.accounts[current_account_id_1]))
        
        # Record the merge in the merged_accounts mapping
        self.merged_accounts[current_account_id_2] = current_account_id_1
        
        # If the original account_id_2 was different from current_account_id_2 (meaning it was already merged)
        # we need to redirect it to the new target as well
        if account_id_2 != current_account_id_2:
            self.merged_accounts[account_id_2] = current_account_id_1
        
        # Record this operation
        self.operations[timestamp] = ("merge_accounts", current_account_id_1, current_account_id_2)
        
        # Mark account_id_2 as deleted
        self.deleted_accounts.add(current_account_id_2)
        if account_id_2 != current_account_id_2:
            self.deleted_accounts.add(account_id_2)
        
        # Remove account_id_2 from the system
        del self.accounts[current_account_id_2]
        del self.outgoing_transactions[current_account_id_2]
        
        return True
        
    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        """
        Returns the account balance at a specific timestamp.
        
        Args:
            timestamp (int): Current timestamp in milliseconds.
            account_id (str): The identifier for the account.
            time_at (int): The timestamp at which to check the balance.
            
        Returns:
            int | None: The account balance at the specified timestamp or None if the account didn't exist.
        """
        # Process any scheduled payments at the current timestamp
        self._process_scheduled_payments(timestamp)
        
        # If the account was deleted and we're checking a time after the deletion,
        # we need to find where it was merged to
        original_account_id = account_id
        
        # Handle the case where we're asking about a deleted account
        if account_id in self.deleted_accounts:
            # Find the account it was merged into, IF the merge happened before time_at
            merge_target = None
            merge_time = float('inf')
            
            # Find the merge operation for this account
            for t, op in sorted(self.operations.items()):
                if t > time_at:
                    break
                if op[0] == "merge_accounts" and op[2] == account_id:
                    merge_target = op[1]
                    merge_time = t
                    break
            
            # If merged before time_at, use the target account
            if merge_target is not None and merge_time <= time_at:
                account_id = merge_target
            else:
                # If checking balance before it was merged, we need the original account's history
                pass
        else:
            # For non-deleted accounts, just get the current ID
            account_id = self._get_current_account_id(account_id)
        
        # Check if account was created after time_at
        for acc_id in [original_account_id, account_id]:
            if acc_id in self.balance_history:
                earliest_time = self.balance_history[acc_id][0][0]
                if earliest_time > time_at:
                    return None
        
        # Check history of the original account ID if available
        if original_account_id in self.balance_history:
            # If the account wasn't merged or we're checking before the merge
            latest_balance = None
            for entry_time, balance in sorted(self.balance_history[original_account_id]):
                if entry_time <= time_at:
                    latest_balance = balance
                else:
                    break
            
            if latest_balance is not None:
                # Check if there was a merge after this time
                merged_after = False
                for t, op in self.operations.items():
                    if op[0] == "merge_accounts" and op[2] == original_account_id and t <= time_at:
                        merged_after = True
                        break
                
                if not merged_after:
                    return latest_balance
        
        # If we get here and the account IDs are different, check the target account's history
        if original_account_id != account_id and account_id in self.balance_history:
            latest_balance = None
            merge_time = 0
            
            # Find when the merge happened
            for t, op in self.operations.items():
                if op[0] == "merge_accounts" and op[1] == account_id and op[2] == original_account_id:
                    merge_time = t
                    break
            
            # Only look at balance entries after the merge
            for entry_time, balance in sorted(self.balance_history[account_id]):
                if merge_time <= entry_time <= time_at:
                    latest_balance = balance
            
            if latest_balance is not None:
                return latest_balance
        
        # If no valid balance found, the account didn't exist at time_at
        return None
    
    def _process_scheduled_payments(self, current_timestamp: int) -> None:
        """
        Processes all scheduled payments that should be executed at or before the current timestamp.
        
        Args:
            current_timestamp (int): The current timestamp in milliseconds.
        """
        # If we've already processed this timestamp, don't process again
        if current_timestamp <= self.last_processed_timestamp:
            return
            
        # Find payments that need to be processed
        payments_to_process = []
        
        for payment_id, payment_data in self.scheduled_payments.items():
            if (payment_data["execution_time"] <= current_timestamp and 
                payment_id not in self.canceled_payments and
                payment_data["execution_time"] > self.last_processed_timestamp):
                # Add to processing queue with execution time and creation timestamp for ordering
                payments_to_process.append({
                    "payment_id": payment_id,
                    "created_at": payment_data["created_at"],
                    "execution_time": payment_data["execution_time"],
                    "account_id": payment_data["account_id"],
                    "amount": payment_data["amount"]
                })
        
        # Sort payments by execution time (primary) and creation timestamp (secondary)
        payments_to_process.sort(key=lambda x: (x["execution_time"], x["created_at"]))
        
        # Process each payment
        for payment in payments_to_process:
            account_id = payment["account_id"]
            amount = payment["amount"]
            execution_time = payment["execution_time"]
            
            # Get current account ID in case of merges
            account_id = self._get_current_account_id(account_id)
            
            # Skip if the account doesn't exist or has insufficient funds
            if (account_id not in self.accounts or 
                self.accounts[account_id] < amount):
                continue
                
            # Process the payment (withdraw money)
            self.accounts[account_id] -= amount
            
            # Track as outgoing transaction
            self.outgoing_transactions[account_id] += amount
            
            # Update balance history
            self.balance_history[account_id].append((execution_time, self.accounts[account_id]))
        
        # Update the last processed timestamp
        self.last_processed_timestamp = current_timestamp
    
    def _get_current_account_id(self, account_id: str) -> str:
        """
        Returns the current account ID, following any merges that may have occurred.
        
        Args:
            account_id (str): The original account ID.
            
        Returns:
            str: The current account ID after following merge history.
        """
        current_id = account_id
        while current_id in self.merged_accounts:
            current_id = self.merged_accounts[current_id]
        return current_id