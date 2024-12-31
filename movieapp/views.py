from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Review
from .models import Movie
from django.contrib import messages
from userapp.models import Customer1


def home(request):
    
    
    movies = Movie.objects.all()  
    paginator = Paginator(movies, 3) 
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  
    return render(request, 'home.html', {'page_obj': page_obj} )

def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()  # Fetch all reviews for the movie
    return render(request, 'movie_details.html', {'movie': movie, 'reviews': reviews})



@login_required
def submit_review(request, movie_id):
    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))
        review_text = request.POST.get("review_text", "").strip()
        created_at=request.POST.get("created_at")
        # Validate rating
        if rating < 1 or rating > 5:
            messages.error(request, 'Rating must be between 1 and 5.')
            return redirect('movieapp:movie_details', movie_id=movie_id)

        movie = get_object_or_404(Movie, id=movie_id)

        # Check if the user already submitted a review
        existing_review = Review.objects.filter(movie=movie, user=request.user).first()

        if existing_review:
            existing_review.rating = rating
            existing_review.review_text = review_text
            existing_review.created_at=created_at
            existing_review.save()
            messages.success(request, 'Your review has been updated successfully!')
        else:
            Review.objects.create(movie=movie, user=request.user, rating=rating, review_text=review_text,created_at=created_at)
            messages.success(request, 'Your review has been submitted successfully!')

        return redirect('movieapp:movie_details', movie_id=movie_id)

    messages.error(request, 'Invalid request method.')
    return redirect('movieapp:movie_details', movie_id=movie_id)
