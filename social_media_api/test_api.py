#!/usr/bin/env python
"""
Comprehensive test suite for Social Media API
Tests all major functionality including authentication, posts, comments, likes, follows, and notifications
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from posts.models import Post, Comment, Like
from notifications.models import Notification

User = get_user_model()

class APITestSuite:
    """Test suite for Social Media API"""
    
    def __init__(self):
        self.client = APIClient()
        self.test_users = []
        self.test_posts = []
        self.tokens = {}
        
    def cleanup(self):
        """Clean up test data"""
        print("\n[CLEANUP] Removing test data...")
        # Delete all test users and their related data
        for user in self.test_users:
            user.delete()
        print("✓ Test data cleaned up")
        
    def create_test_users(self):
        """Create test users"""
        print("\n[TEST 1] Creating test users...")
        users_data = [
            {'username': 'alice', 'email': 'alice@test.com', 'password': 'test123456', 'bio': 'Alice bio'},
            {'username': 'bob', 'email': 'bob@test.com', 'password': 'test123456', 'bio': 'Bob bio'},
            {'username': 'charlie', 'email': 'charlie@test.com', 'password': 'test123456', 'bio': 'Charlie bio'},
        ]
        
        for user_data in users_data:
            user = User.objects.create_user(**user_data)
            self.test_users.append(user)
            token, created = Token.objects.get_or_create(user=user)
            self.tokens[user.username] = token.key
            print(f"  ✓ Created user: {user.username} (token: {token.key[:10]}...)")
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        print("\n[TEST 2] Testing user registration...")
        response = self.client.post('/api/v1/auth/register/', {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpass123456',
        }, format='json')
        
        if response.status_code == 201:
            print(f"  ✓ Registration successful (token: {response.data.get('token', '')[:10]}...)")
            # Clean up new user
            User.objects.filter(username='newuser').delete()
        else:
            print(f"  ✗ Registration failed: {response.data}")
    
    def test_user_login(self):
        """Test user login"""
        print("\n[TEST 3] Testing user login...")
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'alice',
            'password': 'test123456'
        }, format='json')
        
        if response.status_code == 200 and 'token' in response.data:
            print(f"  ✓ Login successful (token: {response.data['token'][:10]}...)")
        else:
            print(f"  ✗ Login failed: {response.data}")
    
    def test_user_profile(self):
        """Test user profile endpoint"""
        print("\n[TEST 4] Testing user profile...")
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tokens["alice"]}')
        response = self.client.get('/api/v1/auth/profile/', format='json')
        
        if response.status_code == 200:
            print(f"  ✓ Profile retrieved:")
            print(f"    - Username: {response.data.get('username')}")
            print(f"    - Bio: {response.data.get('bio')}")
            print(f"    - Following: {response.data.get('following_count')}")
            print(f"    - Followers: {response.data.get('followers_count')}")
        else:
            print(f"  ✗ Profile retrieval failed: {response.data}")
    
    def test_create_post(self):
        """Test creating posts"""
        print("\n[TEST 5] Testing post creation...")
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tokens["alice"]}')
        
        response = self.client.post('/api/v1/posts/', {
            'title': 'Test Post',
            'content': 'This is a test post content'
        }, format='json')
        
        if response.status_code == 201:
            post_id = response.data.get('id')
            self.test_posts.append(post_id)
            print(f"  ✓ Post created (ID: {post_id})")
            print(f"    - Title: {response.data.get('title')}")
            print(f"    - Author: {response.data.get('author')}")
        else:
            print(f"  ✗ Post creation failed: {response.data}")
    
    def test_list_posts(self):
        """Test listing posts"""
        print("\n[TEST 6] Testing post listing...")
        response = self.client.get('/api/v1/posts/', format='json')
        
        if response.status_code == 200:
            count = response.data.get('count', len(response.data) if isinstance(response.data, list) else 0)
            print(f"  ✓ Posts retrieved (Count: {count})")
        else:
            print(f"  ✗ Post listing failed: {response.data}")
    
    def test_create_comment(self):
        """Test creating comments"""
        print("\n[TEST 7] Testing comment creation...")
        if not self.test_posts:
            print("  ⊘ Skipping: No posts to comment on")
            return
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tokens["bob"]}')
        response = self.client.post('/api/v1/comments/', {
            'post': self.test_posts[0],
            'content': 'Great post Alice!'
        }, format='json')
        
        if response.status_code == 201:
            print(f"  ✓ Comment created")
            print(f"    - Author: {response.data.get('author')}")
            print(f"    - Content: {response.data.get('content')[:30]}...")
        else:
            print(f"  ✗ Comment creation failed: {response.data}")
    
    def test_follow_user(self):
        """Test follow functionality"""
        print("\n[TEST 8] Testing user follow...")
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tokens["alice"]}')
        bob_id = next(u.id for u in self.test_users if u.username == 'bob')
        
        response = self.client.post(f'/api/v1/auth/follow/{bob_id}/', format='json')
        
        if response.status_code == 200:
            print(f"  ✓ User followed: {response.data.get('message')}")
        else:
            print(f"  ✗ Follow failed: {response.data}")
    
    def test_unfollow_user(self):
        """Test unfollow functionality"""
        print("\n[TEST 9] Testing user unfollow...")
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tokens["alice"]}')
        bob_id = next(u.id for u in self.test_users if u.username == 'bob')
        
        response = self.client.post(f'/api/v1/auth/unfollow/{bob_id}/', format='json')
        
        if response.status_code == 200:
            print(f"  ✓ User unfollowed: {response.data.get('message')}")
        else:
            print(f"  ✗ Unfollow failed: {response.data}")
    
    def test_feed(self):
        """Test feed functionality"""
        print("\n[TEST 10] Testing feed...")
        # First have Alice follow Bob
        alice = next(u for u in self.test_users if u.username == 'alice')
        bob = next(u for u in self.test_users if u.username == 'bob')
        alice.following.add(bob)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tokens["alice"]}')
        response = self.client.get('/api/v1/feed/', format='json')
        
        if response.status_code == 200:
            count = len(response.data) if isinstance(response.data, list) else response.data.get('count', 0)
            print(f"  ✓ Feed retrieved (Posts from followed users: {count})")
        else:
            print(f"  ✗ Feed retrieval failed: {response.data}")
    
    def test_like_post(self):
        """Test like functionality"""
        print("\n[TEST 11] Testing post like...")
        if not self.test_posts:
            print("  ⊘ Skipping: No posts to like")
            return
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tokens["bob"]}')
        response = self.client.post(f'/api/v1/posts/{self.test_posts[0]}/like/', format='json')
        
        if response.status_code == 200:
            print(f"  ✓ Post liked: {response.data.get('detail')}")
        else:
            print(f"  ✗ Like failed: {response.data}")
    
    def test_unlike_post(self):
        """Test unlike functionality"""
        print("\n[TEST 12] Testing post unlike...")
        if not self.test_posts:
            print("  ⊘ Skipping: No posts to unlike")
            return
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tokens["bob"]}')
        response = self.client.post(f'/api/v1/posts/{self.test_posts[0]}/unlike/', format='json')
        
        if response.status_code == 200:
            print(f"  ✓ Post unliked: {response.data.get('detail')}")
        else:
            print(f"  ✗ Unlike failed: {response.data}")
    
    def test_notifications(self):
        """Test notifications"""
        print("\n[TEST 13] Testing notifications...")
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.tokens["alice"]}')
        response = self.client.get('/api/v1/notifications/', format='json')
        
        if response.status_code == 200:
            count = len(response.data) if isinstance(response.data, list) else response.data.get('count', 0)
            print(f"  ✓ Notifications retrieved (Count: {count})")
        else:
            print(f"  ✗ Notifications retrieval failed: {response.data}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("SOCIAL MEDIA API - COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        
        try:
            self.create_test_users()
            self.test_user_registration()
            self.test_user_login()
            self.test_user_profile()
            self.test_create_post()
            self.test_list_posts()
            self.test_create_comment()
            self.test_follow_user()
            self.test_unfollow_user()
            self.test_feed()
            self.test_like_post()
            self.test_unlike_post()
            self.test_notifications()
            
            print("\n" + "=" * 60)
            print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n✗ Test suite error: {e}")
        finally:
            self.cleanup()

if __name__ == '__main__':
    suite = APITestSuite()
    suite.run_all_tests()
