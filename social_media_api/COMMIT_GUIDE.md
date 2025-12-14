# Commit Guide for Social Media API

This guide helps you commit all changes to your GitHub repository.

## Before Committing

### 1. Verify Everything is Working
```bash
# Run tests
python test_api.py

# Check Django system
python manage.py check

# Review migrations
python manage.py showmigrations
```

### 2. Clean Up (Optional)
```bash
# Remove test database if needed
rm db.sqlite3

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete
```

## Git Configuration (First Time Only)

```bash
# Configure your git identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Navigate to project directory
cd c:\Users\pc gold\Alx_DjangoLearnLab
```

## Commit Steps

### Step 1: Initialize Git Repository (if not already done)
```bash
git init
```

### Step 2: Add All Files
```bash
# Add all files
git add .

# Or add specific files
git add social_media_api/
git add requirements.txt
git add *.md
```

### Step 3: Commit Changes

#### Complete Implementation Commit
```bash
git commit -m "Complete Social Media API Implementation

Tasks Completed:
- Task 0: Project setup and user authentication
- Task 1: Posts and comments functionality
- Task 2: User follows and feed functionality
- Task 3: Notifications and likes functionality
- Task 4: Production deployment

Features:
- Custom user model with follow system
- Complete CRUD for posts and comments
- Dynamic feed based on followed users
- Notifications for user interactions
- Like/unlike post functionality
- Docker and Heroku deployment configuration
- Comprehensive API documentation
- Full test suite (13/13 tests passing)

All endpoints tested and working correctly."
```

### Step 4: Add Remote Repository
```bash
git remote add origin https://github.com/your-username/Alx_DjangoLearnLab.git
```

### Step 5: Push to GitHub
```bash
# First push (set upstream)
git branch -M main
git push -u origin main

# Subsequent pushes
git push origin main
```

## Recommended Commit Messages by Task

### Task 0: User Authentication
```bash
git commit -m "Task 0: Implement user authentication system

- Create custom User model with bio and profile picture
- Implement token-based authentication
- Add registration and login endpoints
- Add user profile management
- Add follow/unfollow functionality
- Create all necessary migrations"
```

### Task 1: Posts and Comments
```bash
git commit -m "Task 1: Implement posts and comments functionality

- Create Post and Comment models
- Add Like model with unique constraint
- Implement CRUD operations for posts and comments
- Add IsAuthorOrReadOnly permission class
- Implement pagination (10 items/page)
- Add search and filtering capabilities
- Create serializers for all models"
```

### Task 2: Follows and Feed
```bash
git commit -m "Task 2: Implement user follows and feed functionality

- Add following field to User model
- Implement follow/unfollow endpoints
- Create dynamic feed view
- Add follower/following counts to profile
- Implement feed filtering and ordering
- Add follow/unfollow validation"
```

### Task 3: Notifications and Likes
```bash
git commit -m "Task 3: Implement notifications and likes

- Create Notification model with GenericForeignKey
- Add Like/Unlike endpoints
- Implement duplicate like prevention
- Create notification list endpoint
- Add mark as read functionality
- Generate notifications on user interactions"
```

### Task 4: Production Deployment
```bash
git commit -m "Task 4: Configure production deployment

- Add Docker containerization
- Create docker-compose.yml with PostgreSQL and Redis
- Configure Nginx reverse proxy with SSL
- Add Heroku Procfile and runtime.txt
- Configure production settings
- Add environment variable support
- Setup WhiteNoise for static files"
```

## Additional Commits (If Making Changes)

### Bug Fix
```bash
git commit -m "Fix: Registration and login endpoints now allow unauthenticated access"
```

### Enhancement
```bash
git commit -m "Enhance: Add Post ordering by creation date in Meta class"
```

### Documentation
```bash
git commit -m "Docs: Add IMPLEMENTATION_COMPLETE.md and VERIFICATION_CHECKLIST.md"
```

## Checking Commit History
```bash
# View commits
git log

# View commits with details
git log --oneline -10

# View specific file history
git log --oneline social_media_api/settings.py
```

## Pushing Updates
```bash
# After making changes
git add .
git commit -m "Description of changes"
git push origin main
```

## Typical Workflow

```bash
# 1. Make changes to code
# ...editing files...

# 2. Check status
git status

# 3. Stage changes
git add .

# 4. Commit with message
git commit -m "Description of changes"

# 5. Push to GitHub
git push origin main

# 6. Verify on GitHub
# Open https://github.com/your-username/Alx_DjangoLearnLab
```

## Tags (Optional - For Releases)

```bash
# Create a tag for task completion
git tag -a v1.0.0-task0 -m "Task 0: User Authentication Complete"
git tag -a v2.0.0-task1 -m "Task 1: Posts and Comments Complete"
git tag -a v3.0.0-task2 -m "Task 2: Follows and Feed Complete"
git tag -a v4.0.0-task3 -m "Task 3: Notifications and Likes Complete"
git tag -a v5.0.0-production -m "Task 4: Production Deployment Complete"

# Push tags
git push origin --tags
```

## Branching Strategy (Advanced)

```bash
# Create feature branch
git checkout -b feature/task0-authentication

# Make commits
git commit -m "Implementation message"

# Merge to main
git checkout main
git merge feature/task0-authentication

# Delete feature branch
git branch -d feature/task0-authentication
```

## Syncing Fork (If Using Fork)

```bash
# Add upstream
git remote add upstream https://github.com/original/Alx_DjangoLearnLab.git

# Fetch updates
git fetch upstream

# Rebase with upstream
git rebase upstream/main

# Push to your fork
git push origin main
```

## Troubleshooting

### Undo Last Commit
```bash
# Keep changes
git reset --soft HEAD~1

# Discard changes
git reset --hard HEAD~1
```

### Push Rejected
```bash
# Pull latest changes
git pull origin main

# Resolve conflicts if any
# Then push again
git push origin main
```

### Wrong Commit Message
```bash
# Amend last commit
git commit --amend -m "New message"
git push origin main -f  # Force push (use carefully!)
```

## .gitignore Content

Your `.gitignore` should already include:
```
*.pyc
__pycache__/
*.py~
*.swp
.DS_Store
venv/
env/
.env
db.sqlite3
.vscode/
.idea/
*.log
staticfiles/
media/
.coverage
htmlcov/
dist/
build/
*.egg-info/
```

## Final Checklist Before Push

- [ ] All tests pass (`python test_api.py`)
- [ ] Django check passes (`python manage.py check`)
- [ ] No syntax errors
- [ ] All documentation updated
- [ ] `.gitignore` properly configured
- [ ] Environment variables not committed
- [ ] Database not committed (except migrations)
- [ ] Virtual environment not committed
- [ ] All meaningful files included
- [ ] Commit message is clear and descriptive

## Success! 🎉

Once you push, your code will be on GitHub and visible at:
```
https://github.com/your-username/Alx_DjangoLearnLab
```

You can share this URL to demonstrate your work!

---

**Need Help?**
- GitHub Documentation: https://docs.github.com/
- Git Tutorial: https://git-scm.com/doc
- Markdown Guide: https://www.markdownguide.org/
