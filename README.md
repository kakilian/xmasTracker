# xmasTracker
Personal Christmas Wishlist Manager with AI Gift Assistant

🎄 **[Live Demo](https://xmastracker.onrender.com/)** 🎄

## Purpose

xmasTracker is a Django-based web application designed to simplify Christmas gift planning and shopping. The platform helps users organize gift ideas for multiple people, track purchases, and get AI-powered gift suggestions. Built with a festive Christmas theme, it combines practical wishlist management with intelligent gift recommendations to make holiday shopping stress-free and organized.

The application solves common holiday gift-giving challenges:
- **Organization**: Keep track of gift ideas for multiple family members and friends in one place
- **Planning**: Add and update gift ideas throughout the year as inspiration strikes
- **Progress Tracking**: Mark items as purchased to avoid duplicate buying
- **Inspiration**: Get personalized AI gift suggestions when you're stuck for ideas
- **Accessibility**: Responsive design works seamlessly on desktop, tablet, and mobile devices

## Planning

### User Stories

1. **Track Multiple People's Wishlists**: As a person who buys gifts for multiple family members or friends, I want to create separate wishlists for each person, so that I can easily keep their gift wishes organized.

2. **Add Wishes Over Time**: As a user who hears gift ideas throughout the year, I want to quickly add new wishes whenever I remember or someone mentions something, so that I don't forget these ideas by Christmas.

3. **Edit & Maintain Lists**: As a user who updates gift plans, I want to edit, reorder, or delete wishlist items, so that each person's list stays accurate and up to date.

4. **View All Wishlists at a Glance**: As a user preparing for Christmas, I want to browse all my saved wishlists easily, so that I can decide what to buy.

5. **Mark Items as Purchased**: As a user, I want to mark wishlist items as "purchased", so that I can track my progress and avoid buying duplicates.

6. **Get Gift Suggestions**: As a user who needs gift ideas, I want to use an AI assistant to generate personalized suggestions based on the recipient's interests, so that I can find the perfect gift.

7. **Save AI Suggestions**: As a user who finds a good AI suggestion, I want to save it directly to a specific person's wishlist, so that I can track it alongside my other gift ideas.

### Entity Relationship Diagram

The database structure consists of three main models:

- **User** (Django AllAuth): Handles authentication and user accounts
- **Wishlist**: Stores wishlist information (person name, auto-generated title, timestamps)
  - One-to-many relationship with User (one user can have many wishlists)
- **WishlistItem**: Stores individual gift ideas (description, URL, notes, priority, purchased status)
  - One-to-many relationship with Wishlist (one wishlist can have many items)
- **SavedGift**: Stores AI-generated suggestions (recipient name, title, description, price range, gift type)
  - Independent table for gift assistant history

### Wireframes

Located in `assets/images/wireframes/` - showing responsive layouts for:
- Homepage with hero section
- Wishlist list view
- Wishlist detail with items
- Gift assistant interface

### Technology Stack

- **Backend**: Django 5.2.8, Python 3.x
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django AllAuth
- **Frontend**: Bootstrap 5.3.3, Bootstrap Icons
- **AI Integration**: OpenAI GPT-4.1-mini
- **Deployment**: Render with Gunicorn and WhiteNoise
- **Version Control**: Git, GitHub

## Features

### Existing Features

#### 1. User Authentication
- **Sign Up**: Create new account with email and password using AllAuth
- **Login/Logout**: Secure authentication with session management
- **Password Reset**: Email-based password recovery (console backend in development)

#### 2. Wishlist Management
- **Create Wishlist**: Simple form asking only for person's name, auto-generates title as "Gift ideas for [Name]"
- **View All Wishlists**: List view showing all wishlists with item count badges
- **Wishlist Detail**: View all items for a specific person with organized card layout

#### 3. Gift Item Management
- **Add Items**: Form with fields for description, URL, notes, and priority level
- **Edit Items**: Update existing gift ideas with pre-filled form
- **Delete Items**: Remove items with confirmation dialog
- **Priority System**: Three-tier priority (High/Medium/Low) with color-coded badges:
  - High: Red badge
  - Medium: Gold badge
  - Low: Blue badge
- **Purchase Tracking**: Toggle purchased status with visual feedback:
  - Purchased items show strikethrough text, gray background, and checkmark icon
  - Click to toggle between purchased/unpurchased states

#### 4. AI Gift Assistant
- **Personalized Suggestions**: Form-based interface collecting:
  - Recipient role (partner, child, parent, sibling, friend, colleague, other)
  - Age range
  - Location
  - Budget range (min/max)
  - Style preferences
  - Interest categories (tech, fashion, sports, etc.)
  - Additional notes
- **AI-Powered Recommendations**: Uses OpenAI GPT-4.1-mini to generate tailored gift ideas
- **Fallback Suggestions**: When API unavailable, provides default suggestion (Cozy Tube Socks)
- **Save to Wishlist**: Dropdown to select which wishlist to save suggestions to
- **Success Messages**: Confirmation when items are saved: "This item was saved to the wishlist for [Name]"

#### 5. Christmas Theme
- **Custom CSS**: Full Christmas color palette:
  - Classic Red (#C1121F) for primary buttons and accents
  - Christmas Green (#0B3D2E) for navbar
  - Frost White (#F7EFEF) for backgrounds
  - Gold (#D4A373) for highlights and medium priority
- **Festive UI**: Christmas emojis in navbar (🎄 🎅 🎁)
- **Responsive Design**: Bootstrap grid system ensures mobile-friendly layouts
- **Visual Enhancements**: Themed badges, alerts, forms, and cards

#### 6. Navigation
- **Auth-Aware Navbar**: Shows different links based on login status
  - Authenticated: My Wishlists, Gift Assistant, User dropdown with logout
  - Guest: Login, Sign Up buttons
- **Quick Access**: Gift Assistant button in wishlist detail pages
- **Breadcrumb Navigation**: Back buttons and clear page hierarchy

### Features Left to Implement

1. **Wishlist Sharing**: Share wishlists with family members or friends
2. **Email Notifications**: Reminders for gift shopping deadlines
3. **Budget Tracking**: Track total spent vs. budget per person
4. **Gift Categories**: Filter and organize by categories (toys, books, electronics)
5. **Shopping Links**: Direct integration with retailers
6. **Gift History**: Archive from previous years
7. **Social Features**: Wishlist discovery and gift recommendations from community

## Bugs

### Fixed Bugs

1. **TemplateSyntaxError - Duplicate Block**: `base.html` had duplicate `{% block content %}` declarations causing template errors
   - **Fix**: Removed duplicate block definition, keeping single content block

2. **OperationalError - No Such Table**: Database tables missing after model creation
   - **Fix**: Ran `python manage.py makemigrations` and `python manage.py migrate`

3. **Logout 405 Method Not Allowed**: GET request to logout URL not supported by AllAuth
   - **Fix**: Changed logout to POST form with CSRF token in `account/logout.html`

4. **AllAuth Deployment Error**: Missing OpenAI API key causing server crash
   - **Fix**: Made OpenAI optional with try/except wrapper, defaults to `None` if key missing

5. **Static Files Not Loading**: Images and CSS not found in production
   - **Fix**: Configured `STATICFILES_DIRS` to include `assets/` directory

6. **Bootstrap Icons Not Visible**: Icon CDN link missing
   - **Fix**: Added Bootstrap Icons 1.11.3 CDN link to `base.html`

7. **Footer Not at Bottom**: Footer floating in middle of page on short content
   - **Fix**: Added `mt-auto` Bootstrap utility class to footer

8. **Form Rendering Error**: AllAuth templates used `add_class` filter without django-widget-tweaks
   - **Fix**: Manually applied Bootstrap classes directly in form HTML

### Known Bugs

1. **SavedGift Model Redundancy**: The `SavedGift` model still exists but is no longer used since suggestions now save directly to `WishlistItem`. Can be removed in future cleanup.

2. **Priority Mapping**: AI suggestions don't automatically map to priority levels - all saved suggestions default to priority 3 (Low). Could enhance by analyzing gift type or price range.

3. **URL Field Validation**: The URL field in `WishlistItem` doesn't validate for proper URL format.

## Code Validation

### Python (PEP 8)
All Python files follow PEP 8 style guidelines:
- `wishlist/views.py`: ✅ Clean
- `wishlist/models.py`: ✅ Clean
- `giftassistant/views.py`: ✅ Clean
- `wishlist/settings.py`: ✅ Clean
- `wishlist/urls.py`: ✅ Clean

### HTML Validation
Templates use Django template syntax and Bootstrap 5 components:
- `base.html`: ✅ Valid structure
- `wishlist/home.html`: ✅ Valid
- `wishlist/wishlist_list.html`: ✅ Valid
- `wishlist/wishlist_detail.html`: ✅ Valid
- `giftassistant/assistant.html`: ✅ Valid
- AllAuth templates: ✅ Valid

### CSS Validation
- `assets/css/christmas-theme.css`: ✅ Valid CSS3 with custom properties

### JavaScript
Minimal JavaScript used (Bootstrap components only) - no custom JS requiring validation.

## Testing

### Manual Testing

| User Story | Test Case | Expected Result | Actual Result | Pass/Fail |
|------------|-----------|-----------------|---------------|-----------|
| Track Multiple People's Wishlists | Create wishlists for 3 different people | Each wishlist appears in list view with correct person name | All wishlists created successfully with auto-generated titles "Gift ideas for [Name]" | ✅ Pass |
| Add Wishes Over Time | Add 5 items to a wishlist with different priorities | Items appear in wishlist detail view sorted by priority | Items display correctly with color-coded priority badges | ✅ Pass |
| Edit & Maintain Lists | Edit item description, change priority, update notes | Changes save and display correctly | All edits persist and show updated information | ✅ Pass |
| Edit & Maintain Lists | Delete item from wishlist | Item removed from list after confirmation | Delete works correctly, item no longer appears | ✅ Pass |
| View All Wishlists at a Glance | Navigate to wishlist list page | See all wishlists with item counts | List displays all wishlists with accurate item count badges | ✅ Pass |
| Mark Items as Purchased | Toggle purchased status on multiple items | Purchased items show strikethrough and gray background | Visual feedback works correctly, toggle persists after page refresh | ✅ Pass |
| Get Gift Suggestions | Fill out gift assistant form with recipient details | AI generates 3-5 relevant gift suggestions | Suggestions appear with title, description, type, and price range | ✅ Pass |
| Get Gift Suggestions (No API) | Use gift assistant without OpenAI API key | Fallback suggestion (Cozy Tube Socks) appears | Fallback gift displays correctly instead of error | ✅ Pass |
| Save AI Suggestions | Select wishlist from dropdown and save suggestion | Item added to chosen wishlist | Suggestion saves successfully, success message displays | ✅ Pass |
| User Authentication | Sign up with new account | Account created, redirected to home | AllAuth signup works, user logged in automatically | ✅ Pass |
| User Authentication | Log out and log back in | Session ends, can log back in | Login/logout flow works correctly | ✅ Pass |
| Responsive Design | View site on mobile (375px width) | All pages responsive, no horizontal scroll | Bootstrap grid adapts correctly, all features accessible | ✅ Pass |
| Responsive Design | View site on tablet (768px width) | Layout adjusts appropriately | Two-column layouts stack, navigation remains usable | ✅ Pass |
| Christmas Theme | Check visual styling across all pages | Christmas colors and theme consistent | Red, green, gold, and frost colors applied throughout | ✅ Pass |

### Browser Compatibility

Tested on:
- ✅ Chrome 131 (Windows)
- ✅ Firefox 133 (Windows)
- ✅ Edge 131 (Windows)
- ✅ Safari (iOS - mobile testing)

### Lighthouse Performance

Homepage scores:
- Performance: 95+
- Accessibility: 100
- Best Practices: 100
- SEO: 100

## Deployment

### Prerequisites

1. Python 3.8+
2. PostgreSQL database (for production)
3. OpenAI API key (optional - for AI gift assistant)
4. Git installed

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kakilian/xmasTracker.git
   cd xmasTracker
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** in project root:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   OPENAI_API_KEY=your-openai-api-key  # Optional
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```

8. Visit `http://127.0.0.1:8000/`

### Deployment to Render

1. **Create Render account** at https://render.com

2. **Create new Web Service**:
   - Connect GitHub repository
   - Select branch: `main`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn wishlist.wsgi:application`

3. **Environment Variables** (Add in Render dashboard):
   ```
   SECRET_KEY=<generate-secure-key>
   DATABASE_URL=<provided-by-render-postgresql>
   ALLOWED_HOSTS=your-app.onrender.com
   DEBUG=False
   OPENAI_API_KEY=<your-key>  # Optional
   PYTHON_VERSION=3.11.0
   ```

4. **Add PostgreSQL Database**:
   - In Render dashboard, create new PostgreSQL database
   - Copy `DATABASE_URL` to environment variables

5. **Deploy**:
   - Render automatically deploys on push to main branch
   - Monitor build logs for any errors
   - Run migrations via Render shell if needed:
     ```bash
     python manage.py migrate
     python manage.py createsuperuser
     ```

### Build Script (`build.sh`)

The included `build.sh` handles deployment tasks:
```bash
#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### Post-Deployment

1. Visit deployed URL
2. Create admin account via Django admin
3. Test all features:
   - User registration/login
   - Wishlist creation
   - Item CRUD operations
   - Gift assistant (if API key configured)

### Forking the Repository

1. Navigate to https://github.com/kakilian/xmasTracker
2. Click "Fork" button (top right)
3. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/xmasTracker.git
   ```

### Making a Local Clone

```bash
git clone https://github.com/kakilian/xmasTracker.git
cd xmasTracker
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Tools & Technologies

- **Django 5.2.8**: Web framework
- **Python 3.x**: Programming language
- **Bootstrap 5.3.3**: Frontend framework
- **PostgreSQL**: Production database
- **SQLite**: Development database
- **Django AllAuth**: Authentication
- **OpenAI API**: AI gift suggestions
- **Gunicorn**: WSGI HTTP server
- **WhiteNoise**: Static file serving
- **Render**: Cloud platform
- **Git/GitHub**: Version control

## Credits

### Team
- **Alex** - [LinkedIn](#)
- **Katarina** - [LinkedIn](#)
- **Fadl** - [LinkedIn](#)

### Resources
- Bootstrap Documentation
- Django Documentation
- OpenAI API Documentation
- AllAuth Documentation
