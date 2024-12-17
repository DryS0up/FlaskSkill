from flask import render_template, request, jsonify, url_for
from models import db, Email, Payment, app
import stripe

# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:mypass@localhost:5432/flaskProject.db'

app.secret_key = "mypass"

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51QWveJKQYw9PlfJFNn2BfY1mjXonH9iamythLVje2TBxPT7lBvMT3fPQZ82dJMcZLp4NhOtR1dcAYvaRTVv4EZ6G00pTi4k3xy'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51QWveJKQYw9PlfJFFkesffnxHEjz3w20ucizZDZ7BoMOVcHRusjpbFLlGQ7xpxtJMi679HsoWxk2WJZH9O628wzb00yOQDwmud'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

@app.route('/')
def Landing():
    return render_template("landing.html")



@app.route('/get-emails', methods=['GET'])
def get_emails():
    emails = Email.query.all()
    email_list = list(map(lambda x: x.to_json(), emails))
    return jsonify({"emails": email_list})



@app.route('/collect-email', methods=['POST'])
def collect_email():
    email = request.json.get('email')

    if not email:
        return jsonify({"message": "Email is required."}), 400

    emailobj = Email(email=email)
    try:
        db.session.add(emailobj)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Email Collected."}), 201




@app.route('/process-payment', methods=['POST'])
def process_payment():
    email = request.json.get('email')
    token = request.json.get('token')

    if not email or not token:
        return jsonify({"message": "Email and Stripe token are required."}), 400

    try:
        payment_method = {
            'type': 'card',
            'card': {
                'token': token  
            }
        }
        payment_intent = stripe.PaymentIntent.create(
            amount=30000,  
            currency='usd',
            payment_method_data=payment_method,  
            confirm=True,  
            receipt_email=email,
            automatic_payment_methods={
                'enabled': True,  
                'allow_redirects': 'never'  
            },
        )
        payment = Payment(
            email=email,
            amount=300,  
            stripe_id=payment_intent.id
        )
        db.session.add(payment)
        db.session.commit()
        return jsonify({"success": True, "message": "Payment processed successfully."})

    except stripe.error.CardError as e:
        return jsonify({"message": f"Payment failed: {e.user_message}"}), 402
    except stripe.error.StripeError as e:
        return jsonify({"message": f"Stripe error: {e.user_message}"}), 500
    except Exception as e:
        return jsonify({"message": f"Error processing payment: {str(e)}"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
