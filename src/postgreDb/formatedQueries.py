"""@package postgreDb
Preformated queries used for table and index creation.

This module provides several string queries used by the DatabaseWrapper module.
Each queries check first if the table exists before creating them.
Index creation is not tested.
"""

blockTable = '''CREATE TABLE IF NOT EXISTS blocks
				(ID 				BIGINT PRIMARY KEY	NOT NULL,
				MAGIC_ID			VARCHAR(8)			NOT NULL,
				LENGTH				INT					NOT NULL,
				VERSION				INT					NOT NULL,
				PREVIOUS_BLOCK_HASH	VARCHAR(64)			NOT NULL,
				MERKLE_ROOT			VARCHAR(64)			NOT NULL,
				TARGET_DIFFICULTY	INT					NOT NULL,
				NONCE				BIGINT				NOT NULL,
				BLOCK_HASH			VARCHAR(64)			NOT NULL,
				FILE_NAME			VARCHAR(50)			NOT NULL,
				REAL_SIZE			BIGINT				NOT NULL,
				BLOCK_TIMESTAMP		TIMESTAMP			NOT NULL,
				REAL_NUMBER			BIGINT				DEFAULT NULL,
				ORPHAN				BOOLEAN				DEFAULT NULL,
				NEXT_BLOCK_HASH		VARCHAR(64)			DEFAULT NULL
				);'''

transactionTable = '''CREATE TABLE IF NOT EXISTS transactions
				(ID 				BIGSERIAL PRIMARY KEY	NOT NULL,
				BLOCK_ID	 		BIGINT 				references blocks(ID),
				VERSION				BIGINT				NOT NULL,
				INPUT_COUNT			BIGINT				NOT NULL,
				OUTPUT_COUNT		BIGINT				NOT NULL,
				LOCKTIME			BIGINT				NOT NULL,
				TRANSACTION_HASH	VARCHAR(64)			NOT NULL
				);'''

inputTable = '''CREATE TABLE IF NOT EXISTS inputs
				(ID 				BIGSERIAL PRIMARY KEY	NOT NULL,
				TRANSACTION_ID 		BIGINT 				references transactions(ID),
				TRANSACTION_HASH	VARCHAR(64)			NOT NULL,
				TRANSACTION_INDEX	BIGINT				NOT NULL,
				COINBASE			BOOLEAN				NOT NULL,
				SEQUENCE_NUMBER		BIGINT				NOT NULL,
				SCRIPT				TEXT				NOT NULL,
				ORPHAN				BOOLEAN				DEFAULT NULL
				);'''

outputTable = '''CREATE TABLE IF NOT EXISTS outputs
				(ID 				BIGSERIAL PRIMARY KEY	NOT NULL,
				TRANSACTION_ID 		BIGINT 				references transactions(ID),
				VALUE				BIGINT				NOT NULL,
				ADDRESS				VARCHAR(34)			NOT NULL,
				SCRIPT				TEXT				NOT NULL,
				INDEX				BIGINT				NOT NULL,
				ORPHAN				BOOLEAN				DEFAULT NULL
				);'''

clusterTable = '''CREATE TABLE IF NOT EXISTS clusters
				(ID					BIGSERIAL PRIMARY KEY	NOT NULL,
				CURRENCY_AMOUNT		BIGINT
				);'''

addressTable = '''CREATE TABLE IF NOT EXISTS addresses
				(ID					VARCHAR(34) PRIMARY KEY NOT NULL,
				CLUSTER_ID			BIGINT				references clusters(ID)
				);'''

ledgerTable = '''CREATE TABLE IF NOT EXISTS ledger
				(ID					BIGSERIAL PRIMARY KEY	NOT NULL,
				ADDRESS				VARCHAR(34)			NOT NULL,
				OPERATION			BOOLEAN				NOT NULL,
				VALUE				BIGINT				NOT NULL,
				BLOCK_TIMESTAMP		TIMESTAMP			NOT NULL
				);'''

transactionIndex = '''CREATE INDEX transactions_idx ON transactions
					(transaction_hash);'''

outputIndex = '''CREATE INDEX outputs_idx ON outputs
					(transaction_id);'''

blockTableDescription = '''SELECT	column_name,
									data_type,
									character_maximum_length
							FROM	information_schema.columns
							WHERE	table_name ='blocks'
						;'''