# Flask ML Ad Dashboard

### Steps to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create MySQL DB:
   ```bash
   mysql -u root -p < schema.sql
   ```

3. Train the model:
   ```bash
   python train_model.py
   ```

4. Run Flask app:
   ```bash
   python app.py
   ```

5. Open http://127.0.0.1:5000 in your browser.
