from django.db.models import Q
from .models import Hospital, Children, Vaccine
from .serializers import HospitalSerializer, ChildrenSerializer, VaccineSerializer
from django.http import JsonResponse
from rest_framework import status
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import datetime


import jwt
from rest_framework.authentication import get_authorization_header


# jwt utilities
def generate_token(hospital_id):
    return jwt.encode({"hospital_id": hospital_id}, "secret", algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, "secret", algorithms=["HS256"])


def authenticate_request(request):
    token = get_authorization_header(request).split()
    token = token[1].decode("utf-8")
    hospital = decode_token(token)
    hospital = Hospital.objects.get(id=hospital["hospital_id"])
    return hospital


# add vaccination records
def add_vaccination_records(birth_date, children_id, hospital_id):
    vaccination_table = [
        (0, "BCG, Hep B1, OPV"),
        (6, "DTwP /DTaP1, Hib-1, IPV-1, Hep B2, PCV 1, Rota-1"),
        (10, "DTwP /DTaP2, Hib-2, IPV-2, Hep B3, PCV 2, Rota-2"),
        (14, "DTwP /DTaP3, Hib-3, IPV-3, Hep B4, PCV 3, Rota-3*"),
        (26, "Influenza-1"),
        (30, "Influenza-2"),
        (27, "Typhoid Conjugate Vaccine"),
    ]

    today = datetime.date.today()
    age_in_weeks = int((today - birth_date).days / 7)

    vaccinations = []

    for duration, vaccine_name in vaccination_table:
        if age_in_weeks >= duration:
            vaccine = {
                "children": children_id,
                "hospital": hospital_id,
                "date": (birth_date + datetime.timedelta(weeks=duration)),
                "vaccine_name": vaccine_name,
            }

            vaccinations.append(vaccine)

    serializer = VaccineSerializer(data=vaccinations, many=True)

    if serializer.is_valid():
        print(serializer.data)
        serializer.save()


# authenticate hospital login
def hospital_authenticate(email, password):
    try:
        hospital = Hospital.objects.get(Q(email=email) & Q(password=password))

    except Hospital.DoesNotExist:
        return None

    return hospital


# --------------------- --------------------------


# register hospital
@csrf_exempt
def hospital_register(request):
    if request.method == "POST":
        try:
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            serializer = HospitalSerializer(data=python_data)

            if serializer.is_valid():
                serializer.save()

                token = generate_token(serializer.data["id"])

                serializer = serializer.data
                del serializer["password"]

                return JsonResponse(
                    {
                        "success": True,
                        "data": serializer,
                        "token": token,
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                return JsonResponse(
                    {"success": False, "error": serializer.errors},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        except Exception as e:
            return JsonResponse(
                {"status": False, "error": e.args},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

    else:
        return JsonResponse(
            {"success": False, "error": "Request not allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# login hospital
@csrf_exempt
def hospital_login(request):
    if request.method == "POST":
        try:
            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)

            email = python_data["email"]
            password = python_data["password"]

            hospital = hospital_authenticate(email, password)

            if hospital is not None:
                serializer = HospitalSerializer(hospital)
                serializer = serializer.data

                token = generate_token(serializer["id"])

                del serializer["password"]

                return JsonResponse(
                    {
                        "success": True,
                        "data": serializer,
                        "token": token,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Invalid email password",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        except KeyError:
            return JsonResponse(
                {"success": False, "error": "Required data not found"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

    else:
        return JsonResponse(
            {"success": False, "error": "Request not allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# register children
@csrf_exempt
def children_register(request):
    if request.method == "POST":
        try:
            hospital = authenticate_request(request)

            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)
            python_data["hospital"] = hospital.id

            serializer = ChildrenSerializer(data=python_data)

            if serializer.is_valid():
                serializer.save()

                add_vaccination_records(
                    datetime.datetime.strptime(
                        serializer.data["dob"], "%Y-%m-%d"
                    ).date(),
                    serializer.data["id"],
                    serializer.data["hospital"],
                )

                return JsonResponse(
                    {"success": True, "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            else:
                return JsonResponse(
                    {"success": False, "error": serializer.errors},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        except Exception as e:
            return JsonResponse(
                {"error": e.args}, status=status.HTTP_406_NOT_ACCEPTABLE
            )

    else:
        return JsonResponse(
            {"success": False, "error": "Request not allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# get children detail by id
@csrf_exempt
def children_detail(request, id):
    try:
        hospital = authenticate_request(request)

        vaccines = Vaccine.objects.filter(hospital=hospital.id, children=id)

        serializer = VaccineSerializer(vaccines, many=True)

        return JsonResponse(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    except KeyError:
        return JsonResponse(
            {"success": False, "error": "Required data not found"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    except Exception as e:
        return JsonResponse({"error": e.args}, status=status.HTTP_406_NOT_ACCEPTABLE)


# update children
@csrf_exempt
def children_update(request, id):
    if request.method == "PUT":
        try:
            hospital = authenticate_request(request)

            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)

            children = Children.objects.get(Q(hospital=hospital.id) & Q(id=id))

            serializer = ChildrenSerializer(children, data=python_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(
                    {"success": True, "data": serializer.data},
                    status=status.HTTP_200_OK,
                )

            else:
                return JsonResponse(
                    {"success": False, "error": serializer.errors},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        except KeyError:
            return JsonResponse(
                {"success": False, "error": "Required data not found"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        except Exception as e:
            return JsonResponse(
                {"error": e.args}, status=status.HTTP_406_NOT_ACCEPTABLE
            )

    else:
        return JsonResponse(
            {"success": False, "error": "Request not allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# get all childrens
@csrf_exempt
def children_list(request):
    try:
        hospital = authenticate_request(request)

        childrens = Children.objects.filter(hospital=hospital.id)

        serializer = ChildrenSerializer(childrens, many=True)

        return JsonResponse(
            {"success": True, "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    except KeyError:
        return JsonResponse(
            {"success": False, "error": "Required data not found"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    except Exception as e:
        return JsonResponse({"error": e.args}, status=status.HTTP_406_NOT_ACCEPTABLE)


# delete children
@csrf_exempt
def children_delete(request, id):
    try:
        hospital = authenticate_request(request)

        children = Children.objects.get(Q(id=id) & Q(hospital=hospital.id))
        children.delete()

        return JsonResponse(
            {"success": True, "data": "Record deleted successsfully"},
            status=status.HTTP_200_OK,
        )

    except KeyError:
        return JsonResponse(
            {"success": False, "error": "Required data not found"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    except Exception as e:
        return JsonResponse({"error": e.args}, status=status.HTTP_406_NOT_ACCEPTABLE)


# get vaccination by date
@csrf_exempt
def vaccination_date(request, date):
    try:
        hospital = authenticate_request(request)

        vaccinations = Vaccine.objects.filter(
            date=datetime.datetime.strptime(date, "%Y-%m-%d").date(),
            hospital_id=hospital.id,
            taken=False,
        ).select_related("children")

        data = []

        for vaccination in vaccinations:
            vaccine_item = {
                "id": vaccination.id,
                "parent_name": vaccination.children.parent_name,
                "parent_email": vaccination.children.parent_email,
                "phone_number": vaccination.children.phone_number,
                "vaccine_name": vaccination.vaccine_name,
                "date": vaccination.date,
                "taken": vaccination.taken,
            }

            data.append(vaccine_item)

        return JsonResponse(
            {"success": True, "data": data},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return JsonResponse({"error": e.args}, status=status.HTTP_406_NOT_ACCEPTABLE)


# update vaccination status (take)
@csrf_exempt
def vaccination_update(request, id):
    if request.method == "PUT":
        try:
            hospital = authenticate_request(request)

            json_data = request.body
            stream = io.BytesIO(json_data)
            python_data = JSONParser().parse(stream)

            python_data["taken"] = True if python_data["taken"] == "True" else False

            vaccine = Vaccine.objects.get(Q(hospital=hospital.id) & Q(id=id))

            serializer = VaccineSerializer(vaccine, data=python_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(
                    {"success": True, "data": serializer.data},
                    status=status.HTTP_200_OK,
                )

            return JsonResponse(
                {"error": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE
            )

        except KeyError:
            return JsonResponse(
                {"success": False, "error": "Required data not found"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        except Exception as e:
            return JsonResponse(
                {"error": e.args}, status=status.HTTP_406_NOT_ACCEPTABLE
            )

    else:
        return JsonResponse(
            {"success": False, "error": "Request not allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )
