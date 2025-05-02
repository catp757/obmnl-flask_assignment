# Import libraries
from flask import Flask, url_for, redirect, request, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation: read all transactions
@app.route('/')
def get_transactions():
    return render_template('index.html', transactions=transactions)

# Create operation: Display add transaction form
# Route to handle the creation of a new transaction
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,            # Generate a new ID based on the current length of the transactions list
            'date': request.form['date'],           # Get the 'date' field value from the form
            'amount': float(request.form['amount']) # Get the 'amount' field value from the form and convert it to a float
        }
        # Append the new transaction to the transactions list
        transactions.append(transaction)

        # Redirect to the transactions list page after adding the new transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, render the form template to display the add transaction form
    return render_template("form.html")

# Update operation: Display edit transaction form
# Route to handle the editing of an existing transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']           # Get the 'date' field value from the form
        amount = float(request.form['amount'])# Get the 'amount' field value from the form and convert it to a float

        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date       # Update the 'date' field of the transaction
                transaction['amount'] = amount   # Update the 'amount' field of the transaction
                break                            # Exit the loop once the transaction is found and updated

        # Redirect to the transactions list page after updating the transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            # Render the edit form template and pass the transaction to be edited
            return render_template("edit.html", transaction=transaction)

    # If the transaction with the specified ID is not found, handle this case (optional)
    return {"message": "Transaction not found"}, 404

# Delete operation: Delete a transaction
# Route to handle the deletion of an existing transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)  # Remove the transaction from the transactions list
            break  # Exit the loop once the transaction is found and removed

    # Redirect to the transactions list page after deleting the transaction
    return redirect(url_for("get_transactions"))

# Search operation: Display transactions searched given a min and max amount
# Route to handle the search functionality
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        
        # Extract the search criteria from the form fields
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])

        filtered_transactions = []  # Initialize an empty list to store filtered transactions
        for transaction in transactions:
            # Check if the transaction amount is within the specified range
            if min_amount <= transaction['amount'] <= max_amount:
                filtered_transactions.append(transaction)

        # Render the search results template and pass the matching transactions
        if filtered_transactions:
            # If there are matching transactions, render the search results template with the filtered transactions
            return render_template("index.html", transactions=filtered_transactions)
        else:
            # If no transactions match the search criteria, render the search results template with an empty list
            return render_template("index.html", transactions=[])
            
    return render_template("search.html")

# Route to handle the balance calculation
# This route is used to calculate and display the total balance of all transactions
@app.route("/balance")
def get_balance():
    # Calculate the total balance by summing the amounts of all transactions
    total_bal= sum(transaction['amount'] for transaction in transactions)
    
    # Render the transactions and the total balance
    return render_template("index.html", transactions=transactions, total_balance=total_bal)

# Run the Flask app
# This block checks if the script is being run directly (not imported as a module)
# and starts the Flask development server with debug mode enabled.
if __name__ == "__main__":
    app.run(debug=True)