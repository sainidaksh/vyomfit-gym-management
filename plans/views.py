from django.shortcuts import render, redirect, get_object_or_404
from .models import Plan
from gyms.models import Gym
from django.db.models import Count

# PLAN LIST
def plans_list(request):
    plans = Plan.objects.annotate(total_sales=Count("subscription")).all()
    return render(request, "plans/list.html", {"plans": plans})

# PLAN CREATE
def plan_create(request):
    if request.method == "POST":
        name = request.POST["name"]
        duration_type = request.POST["duration_type"]
        duration_value = int(request.POST["duration_value"])
        price = request.POST["price"]
        description = request.POST["description"]
        gym = Gym.objects.first()

        Plan.objects.create(
            gym=gym,
            name=name,
            duration_type=duration_type,
            duration_value=duration_value,
            price=price,
            description=description
        )

        return redirect("plans_list")

    return render(request, "plans/create.html")



# PLAN EDIT
def plan_edit(request, id):
    plan = get_object_or_404(Plan, id=id)

    if request.method == "POST":
        plan.name = request.POST["name"]
        plan.duration_type = request.POST["duration_type"]
        plan.duration_value = int(request.POST["duration_value"])
        plan.price = request.POST["price"]
        plan.description = request.POST["description"]
        plan.save()

        return redirect("plans_list")

    return render(request, "plans/edit.html", {"plan": plan})


# PLAN DELETE
def plan_delete(request, id):
    plan = get_object_or_404(Plan, id=id)
    plan.delete()
    return redirect("plans_list")
