web: gunicorn my_project.wsgi
Bugs Encountered and Fixes
1. Missing Recipe and Comment Models
Issue: models.py was empty
Fix: Created Recipe (with author ForeignKey) and Comment (linked to recipes and users) models; ran migrations
2. Missing Recipe Forms
Issue: No forms for creating/editing recipes or commenting
Fix: Created forms.py with RecipeForm and CommentForm using Django ModelForms
3. Missing Recipe Templates
Issue: No UI templates for recipe list, detail view, or forms
Fix: Created base.html, recipe_list.html, recipe_detail.html, and recipe_form.html
4. Missing CSRF Token in Signup
Issue: Signup form submissions failing
Fix: Added {% csrf_token %} to the signup template
5. Line Length Style Violations
Issue: Lines in views.py and urls.py exceeded 79 characters
Fix: Wrapped long lines across multiple lines
6. Missing HttpResponse Import
Issue: views.py used HttpResponse without importing it
Fix: Added from django.http import HttpResponse
7. Unused Comment Import
Issue: Comment imported but never used in views.py
Fix: Removed unused import
8. Signup 500 Error
Issue: User reported server error on signup
Fix: Testing confirmed signup working correctly (302 redirects); issue resolved by implementing proper views and templates