# 🥗 Meal Analyzer - AI-Powered Food Calorie Counter

A simple web app that analyzes food photos and provides calorie estimates using Claude AI.

## Features

- 📸 Take or upload photos of meals
- 🤖 AI identifies foods and portion sizes
- 🔥 Instant calorie calculations
- 📱 Mobile-friendly interface
- ✨ Clean, modern design

## How It Works

1. User takes/uploads a photo of their meal
2. Image is sent to Claude AI (via Anthropic API)
3. Claude identifies each food item, estimates portions, and calculates calories
4. Results are displayed in an easy-to-read format

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- An Anthropic API key (get one at https://console.anthropic.com/)

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your Anthropic API key:**
   
   **Option A - Environment Variable (recommended):**
   ```bash
   # On Mac/Linux:
   export ANTHROPIC_API_KEY='your-api-key-here'
   
   # On Windows:
   set ANTHROPIC_API_KEY=your-api-key-here
   ```
   
   **Option B - Edit app.py:**
   Open `app.py` and replace `'your-api-key-here'` with your actual API key on line 14.

3. **Run the server:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

5. **Start analyzing meals!**
   - Click "Choose Photo"
   - Take a picture or select an existing photo
   - Click "Analyze Meal"
   - Get instant results!

## Usage

### On Your Phone
1. Open `http://localhost:5000` in your phone's browser (make sure you're on the same WiFi network as your computer)
2. You might need to use your computer's IP address instead of localhost, like `http://192.168.1.10:5000`

### Sharing with Others
If you want your wife's sister or others to use it:
- Keep the app running on your computer
- Share your local IP address (find it with `ipconfig` on Windows or `ifconfig` on Mac/Linux)
- They can access it at `http://YOUR-IP:5000`

## Cost Estimate

Using Claude API:
- Approximately $0.01-0.03 per image analysis
- For personal use (10-20 photos/day), expect $5-15/month

## Making It Public (Optional Future Step)

If this gets popular, you can deploy it to a service like:
- **Vercel** (easy, free tier available)
- **Railway** (simple, great for Python)
- **Heroku** (classic choice)
- **Replit** (easiest for beginners)

## Customization Ideas

Want to make it better? Here are some ideas:

1. **Save history**: Store analysis results in a database
2. **User accounts**: Track meals over time
3. **Daily totals**: Sum up calories for the day
4. **Meal tracking**: Name and save meals for reuse
5. **Nutrition macros**: Add protein, carbs, fat breakdown
6. **Export data**: Download CSV of meal history

## Troubleshooting

**"Failed to analyze image"**
- Check your API key is set correctly
- Verify you have internet connection
- Make sure the image is clear and shows food

**Can't access from phone**
- Ensure phone and computer are on same WiFi
- Use computer's IP address instead of localhost
- Check if firewall is blocking port 5000

**Images not uploading**
- Try a smaller image size
- Check file format (JPG, PNG work best)
- Verify camera permissions on your phone

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Backend**: Python, Flask
- **AI**: Claude 4 Sonnet (via Anthropic API)
- **Image Processing**: Pillow (PIL)

## Privacy Note

Images are sent to Anthropic's servers for analysis. If privacy is a concern, you could:
- Run a local AI model instead (more complex)
- Use a self-hosted solution
- Add a disclaimer for users

## License

Free for personal use. Do whatever you want with it!

## Support

If you run into issues:
1. Check the console/terminal for error messages
2. Verify your API key is correct
3. Try a different image
4. Make sure all dependencies are installed

---

Built with ❤️ for tracking meals and staying healthy!
