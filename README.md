
## Children Vaccination Shceduler

The Children Vaccination System is a application designed to streamline and manage the vaccination process for newborn children. It provides a centralized platform for hospitals to register children, maintain vaccination records, and facilitate communication with parents. The system aims to ensure that children receive timely vaccinations according to the recommended schedule, thereby promoting their health and well-being.

### Key Features:

#### 1) Registration and Profile Management:
#### 2) Admin Panel:
#### 3) Child Profile Management:
#### 4) Security and Authentication:

## API Reference

#### Hospital registration

```http
  POST /api/hospital-register/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name`    | `string` | **Required**. name of hospital |
| `phone_number`    | `number` | **Required**. phone number of hospital |
| `email`    | `email` | **Required & Unique**. email of hospital |
| `password`    | `string` | **Required**. password for admin account |

#### Response
```JSON
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Hospital Name",
        "phone_number": 0000000000,
        "email": "hospital_name@gmail.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJob3NwaXRhbF9pZCI6OH0.5IWfIMulXkqZplLLUPzv0zaeAqu0srIcujdFnPxzPn4"
}
```

#### Hospital login

```http
  POST /api/hospital-login/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email`    | `email` | **Required**. email of hospital |
| `password`    | `string` | **Required**. password of admin account |

#### Response
```JSON
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Hospital Name",
        "phone_number": 0000000000,
        "email": "hospital_name@gmail.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJob3NwaXRhbF9pZCI6OH0.5IWfIMulXkqZplLLUPzv0zaeAqu0srIcujdFnPxzPn4"
}
```

## All the following api routes requires Authorization header

#### Children registration

```http
  POST /api/children-register/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `dob`    | `date` | **Required**. (%Y-%M-%D) |
| `gender`    | `string` | **Required**. (M or F) |
| `parent_name`    | `string` | **Required**. |
| `parent_email`    | `string` | **Required**. |
| `phone_number`    | `number` | **Required**. |

#### Response
```JSON
{
    "success": true,
    "data": {
        "id": 25,
        "dob": "2002-09-15",
        "gender": "M",
        "parent_name": "parent name",
        "parent_email": "parent_email@gmail.com",
        "phone_number": 0000000000,
        "hospital": 8
    }
}
```

#### Children detail

```http
  GET /api/children-detail/<id>
```

#### Response
```JSON
{
    "success": true,
    "data": [
        {
            "id": 22,
            "children": 25,
            "hospital": 8,
            "date": "2002-09-15",
            "vaccine_name": "BCG, Hep B1, OPV",
            "taken": true
        },
        {
            "id": 23,
            "children": 25,
            "hospital": 8,
            "date": "2002-10-27",
            "vaccine_name": "DTwP /DTaP1, Hib-1, IPV-1, Hep B2, PCV 1, Rota-1",
            "taken": false
        },
        {
            "id": 24,
            "children": 25,
            "hospital": 8,
            "date": "2002-11-24",
            "vaccine_name": "DTwP /DTaP2, Hib-2, IPV-2, Hep B3, PCV 2, Rota-2",
            "taken": false
        },
        {
            "id": 25,
            "children": 25,
            "hospital": 8,
            "date": "2002-12-22",
            "vaccine_name": "DTwP /DTaP3, Hib-3, IPV-3, Hep B4, PCV 3, Rota-3*",
            "taken": false
        },
        {
            "id": 26,
            "children": 25,
            "hospital": 8,
            "date": "2003-03-16",
            "vaccine_name": "Influenza-1",
            "taken": false
        },
        {
            "id": 27,
            "children": 25,
            "hospital": 8,
            "date": "2003-04-13",
            "vaccine_name": "Influenza-2",
            "taken": false
        },
        {
            "id": 28,
            "children": 25,
            "hospital": 8,
            "date": "2003-03-23",
            "vaccine_name": "Typhoid Conjugate Vaccine",
            "taken": false
        }
    ]
}
```

#### Children list

```http
  GET /api/children-list/
```

#### Response
```JSON
{
    "success": true,
    "data": [
        {
            "id": 24,
            "dob": "2002-09-15",
            "gender": "M",
            "parent_name": "parent name",
            "parent_email": "parent_email@gmail.com",
            "phone_number": 0000000000,
            "hospital": 8
        }
    ]
}
```

#### Delete children

```http
  DELETE /api/children-delete/<id>
```

#### Response
```JSON
{
    "success": true,
    "data": "Record deleted successsfully"
}
```

#### Get all vaccination of given date

```http
  GET /api/vaccination-date/<date>
```

#### Response
```JSON
{
    "success": true,
    "data": [
        {
            "id": 15,
            "parent_name": "parent name",
            "parent_email": "parent_email@gmail.com",
            "phone_number": 0000000000,
            "vaccine_name": "BCG, Hep B1, OPV",
            "date": "2002-09-15",
            "taken": false
        }
    ]
}
```

#### Update vaccination status

```http
  PUT /api/children-register/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `taken`    | `string` | **Required**. ("True" or "False") |

#### Response
```JSON
{
    "success": true,
    "data": {
        "id": 22,
        "children": 25,
        "hospital": 8,
        "date": "2002-09-15",
        "vaccine_name": "BCG, Hep B1, OPV",
        "taken": true
    }
}
```
