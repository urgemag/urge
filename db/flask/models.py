***REMOVED*** Functions of the !--Urge--! panel ! ***REMOVED***
# pylint: disable=R0913
import hashlib
import random
import pymongo
import re
from math import ceil
from os import mkdir, path, remove, system, rename
from PIL import Image
import filetype
import setting
import requests
import ast
import json 
from pprint import pprint
from datetime import *

# it uses << imgp >> too


class General:
    ***REMOVED*** These are the functions which will be used in others and they are general ! ***REMOVED***

    def __init__(self):
        self.special_characters = ['!', ' ', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '/', ':', ';', '=', '?', '@', '[', ']', "'", '!', '#', '$', '&', "'", '(', ')', '*', '+', ',', '/', ':', ';', '=', '?', '@', '[', ']', '%', '<', '>', '^', '_', '`', '{', '|', '}', '~', '£', '円']

    @classmethod
    def sha256_hash(cls, password):
        ***REMOVED*** To hash passwords or others with sha256 method ***REMOVED***
        result = hashlib.sha256(password.encode("utf-8"))
        return result.hexdigest()

    def sha256_hash_bytes(cls, file_bytes):
        ***REMOVED*** To hash bytes with sha256 method ***REMOVED***
        result = hashlib.sha256(file_bytes).hexdigest()
        return result

    def format_recognizer(self, file):
        return str(filetype.guess_extension(file))

    def size_image_file(self, image_path):
        image = Image.open(image_path)
        width, height = image.size
        return width, height

    def image_resizer_using_pil(self, image_path, basewidth=1500):

        img = Image.open(image_path)
        wpercent = basewidth / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(image_path)

    def image_resizer_using_imgp(self, image_path, basewidth=1500):
        command = "imgp -x {width}x{width} '{path}'".format(
            width=basewidth, path=image_path
        )
        system(command)
        new_file_name = (
            ("/".join((image_path.split("/")[:-1]) + ([""])))
            + (".".join(image_path.split("/")[-1].split(".")[:-2] + [""]))
            + image_path.split("/")[-1].split(".")[-2]
            + "_IMGP"
            + "."
            + image_path.split("/")[-1].split(".")[-1]
        )
        try:
            rename(new_file_name, image_path)
        except FileNotFoundError:
            pass

    def image_optimizer_using_imgp(self, image_path):
        command = "imgp -p '{path}'".format(path=image_path)
        system(command)
        new_file_name = (
            ("/".join((image_path.split("/")[:-1]) + ([""])))
            + (".".join(image_path.split("/")[-1].split(".")[:-2] + [""]))
            + image_path.split("/")[-1].split(".")[-2]
            + "_IMGP"
            + "."
            + image_path.split("/")[-1].split(".")[-1]
        )
        rename(new_file_name, image_path)

    def logo_merger(self, image_path):
        location_urge_logo = "static/assets/images/logo/Logo.png"

        image = Image.open(image_path)
        logo = Image.open(location_urge_logo)
        image_copy = image.copy()

        position = (
            (image_copy.width - logo.width - 5),
            (image_copy.height - logo.height - 5),
        )
        image_copy.paste(logo, position, logo)
        image_copy.save(image_path)

    def valid_email(self, email):
        ***REMOVED*** Check if an email is valid or not ***REMOVED***
        return bool(
            re.search(
                r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$",
                General().corect_form_of_email(email),
            )
        )

    def corect_form_of_email(self, email):
        ***REMOVED*** return Email without Dots and uppercases ***REMOVED***
        print(email)
        email_correct = email.lower()
        email_seprated = email_correct.split("@")
        email_seprated[0] = email_seprated[0].replace(".", "")
        email_correct = email_seprated[0] + "@" + email_seprated[1]
        return email_correct

    def save_picture_of_course(self, slug, uploaded_file):
        href = "/static//assets/images/courses/{slug}/{name}"
        try:
            mkdir("static/assets/images/courses/{slug}".format(slug=slug))
        except:
            pass

        pic_format = ((uploaded_file.filename).split("."))[-1]
        pic_format = pic_format.lower()
        if pic_format not in ["jpg", "jpeg", "png", "webp"]:
            return {"Message": "فرمت فایل باید تصویر باشد.", "Result": False}
        name = "{slug}-course-picture_medium-size.{the_format}".format(
            slug=slug, the_format=pic_format
        )
        if (
            path.exists(
                "static/assets/images/courses/{slug}/{slug}-course-picture_medium-size.{the_format}".format(
                    slug=slug, the_format=pic_format
                )
            )
            is False
        ):
            location_not_href = "static/assets/images/courses/{slug}/{slug}-course-picture_medium-size.{the_format}".format(
                slug=slug, the_format=pic_format
            )
            href = "/static//assets/images/courses/{slug}/{slug}-course-picture_medium-size.{the_format}".format(
                slug=slug, the_format=pic_format
            )
        else:
            counter = 0
            while True:
                if (
                    path.exists(
                        "static/assets/images/courses/{slug}/{slug}-course-picture_medium-size-{num}.{the_format}".format(
                            slug=slug, num=str(counter), the_format=pic_format
                        )
                    )
                    is True
                ):
                    counter += 1
                else:
                    location_not_href = "static/assets/images/courses/{slug}/{slug}-course-picture_medium-size-{num}.{the_format}".format(
                        slug=slug, num=str(counter), the_format=pic_format
                    )
                    href = "/static//assets/images/courses/{slug}/{slug}-course-picture_medium-size-{num}.{the_format}".format(
                        slug=slug, num=str(counter), the_format=pic_format
                    )
                    break

        uploaded_file.save(location_not_href)
        General().image_resizer_using_pil(location_not_href,500)

        return {"path": location_not_href, "href": href, "Result": True}

        #   resize them , save multiple maybe.

    def save_music_of_day(self, slug, day, music):

        music_filename = music.filename
        for character in music_filename:
            if character in self.special_characters:
                music_filename = music_filename.replace(character, "")

        try:
            mkdir("static/assets/musics/" + str(slug))
        except:
            pass

        try:
            mkdir("static/assets/musics/" + str(slug) + "/" + str(day))
        except:
            pass

        location_image = (
            "static/assets/musics/" + str(slug) + "/" + str(day) + "/" + music_filename
        )
        location_image_href = (
            "/static//assets/musics/"
            + str(slug)
            + "/"
            + str(day)
            + "/"
            + music_filename
        )

        music.save(location_image)

        return {
            "href": location_image_href,
            "image": location_image,
        }

    def save_music_cover_of_day(self, cover_bytes):

        hash_image = General().sha256_hash_bytes(cover_bytes)

        format_file = General().format_recognizer(cover_bytes)
        file_name = "music_cover_of_day_" + str(hash_image) + "." + format_file
        location_image = "static/assets/images/days_of_course/music_covers/" + file_name
        location_image_href = (
            "/static//assets/images/days_of_course/music_covers/" + file_name
        )
        with open(location_image, "wb") as file:
            file.write(cover_bytes)

        General().image_resizer_using_imgp(location_image, 500)

        return {"href": location_image_href, "image": location_image}

    def save_podcast_cover_of_day(self, cover_bytes):

        hash_image = General().sha256_hash_bytes(cover_bytes)

        format_file = General().format_recognizer(cover_bytes)
        file_name = "podcast_cover_of_day_" + str(hash_image) + "." + format_file
        location_image = (
            "static/assets/images/days_of_course/podcast_covers/" + file_name
        )
        location_image_href = (
            "/static//assets/images/days_of_course/podcast_covers/" + file_name
        )
        with open(location_image, "wb") as file:
            file.write(cover_bytes)

        General().image_resizer_using_imgp(location_image, 500)

        return {"href": location_image_href, "image": location_image}

    def remove_file(self, path):
        try:
            remove(path)
            return True
        except:
            return False

    def price_beautifier(self,price_couese):
        price=int(str(price_couese).replace(",", ""))
        List=[]
        for i in (str(price)):
            List.append(i)
        for x in range ((len(str(price))-1)//3):
            count = (x+1) * 3
            List.insert(len(str(price))-count,",")
        return ("".join(List))

    def days_passed_till_now(self):
        now_date = date.today()
        zero_date = date(1, 1, 1)
        delta_date = now_date-zero_date
        return int(delta_date.days)

class Authentication:
    ***REMOVED*** Authentications of the urge panel ! ***REMOVED***

    def __init__(self, session=None):
        ***REMOVED*** Get session to be used in some of the functions for the authentications. ***REMOVED***
        self.session = session

    @classmethod
    def signup(cls, first_name, last_name, email, password):
        ***REMOVED*** To signup => check if Email is unique, password is suitable, email is correct. ***REMOVED***

        if email == "" or email is None:
            return {"result": False, "message": " ایمیلتان را وارد کنید. "}

        if General().valid_email(email) is False:
            return {"result": False, "message": " فرمت ایمیل اشتباه است. "}

        if first_name == "" or first_name is None:
            return {"result": False, "message": " نامتان را وارد کنید. "}

        if last_name == "" or last_name is None:
            return {"result": False, "message": " نام خانوادگیتان را وارد کنید. "}

        # Check if email is already taken
        if (
            Database().get_users_data_from_db(General().corect_form_of_email(email))
            is not False
        ):
            return {"result": False, "message": " ایمیل قبلا ثبت شده است. "}

        # Check Password Length
        if len(str(password)) < 8:
            return {"result": False, "message": " پسسورد حداقل باید 8 کاراکتر باشد. "}

        # If There was no problem , Here We will sign the data up into the DataBase
        if Database().add_users_data_to_db(
            email,
            General().sha256_hash(password),
            first_name,
            last_name,
        ):
            return {
                "result": True,
                "message": " شما با موفقیت ثبت نام شدید. ",
                "session": {"Email": General().corect_form_of_email(email)},
            }

        return {
            "result": False,
            "message": " ظاهرا مشکلی پیش اومده. لطفا اطلاعات را صحیح وارد کنید. ",
        }

    @classmethod
    def signin(cls, username_or_email, password):
        ***REMOVED*** To signin => check if username matches the password. ***REMOVED***
        data = Database().get_users_data_from_db(
            General().corect_form_of_email(username_or_email)
        )
        if data == False:
            return {"result": False, "message": " ایمیل یا پسوورد اشتباه است. "}
        hash_password = General().sha256_hash(password)
        if data["Password"] == hash_password:
            return {
                "result": True,
                "message": " شما با موفقیت ثبت نام شدید. ",
                "session": {
                    "Email": General().corect_form_of_email(
                        General().corect_form_of_email(username_or_email)
                    )
                },
            }

        return {"result": False, "message": " ایمیل یا پسوورد اشتباه است. "}

    def unique_username(self, username):
        ***REMOVED*** To check if the username is unique and not taken. ***REMOVED***

    def email_verification(self):
        ***REMOVED*** To send a random code to the email address and verify the email. ***REMOVED***

    def mobile_number_verification(self):
        ***REMOVED*** To send a random code to the phone number and verify the number. ***REMOVED***

    def forget_password_by_email(self):
        ***REMOVED***To send a random code to the email address and
        after the verification, change the password.***REMOVED***

    @classmethod
    def change_password(cls):
        ***REMOVED*** To change the password. ***REMOVED***

    def is_signed_in(self):
        ***REMOVED*** check the cookies out to see if the account is active and logged in or not. ***REMOVED***
        if self.session.get("logged_in"):
            return True
        return False
    
    def is_admin(self):
        ***REMOVED*** check the cookies out to see if the account is admin or not. ***REMOVED***
        if Authentication(self.session).is_signed_in() and self.session.get("admin"):
            return True
        return False


class Database:
    ***REMOVED*** Every functions that work with database ( MongoDB ) ! ***REMOVED***

    def __init__(self):
        ***REMOVED*** Get session to be used in some of the functions for the Database. ***REMOVED***
        self.database = pymongo.MongoClient(setting.mongodb_URI)["urge_panel"]

    def get_users_data_from_db(self, email):
        ***REMOVED*** To get users data from the DataBase***REMOVED***
        if (
            self.database.users.find_one(
                {"Email": General().corect_form_of_email(email)}
            )
            is None
        ):
            return False
        return self.database.users.find_one(
            {"Email": General().corect_form_of_email(email)}
        )

    def get_users_access_data_from_db(self, email):
        ***REMOVED*** To get users accesses from the DataBase***REMOVED***
        if email == "" or email is None or "@" not in email:
            return []
        if (
            self.database.users.find_one(
                {"Email": General().corect_form_of_email(email)}
            )
            is None
        ):
            return []
        user_data = self.database.users.find_one(
            {"Email": General().corect_form_of_email(email)}
        )
        if "Accesses" in user_data:
            return user_data["Accesses"]

        return []

    def get_all_courses_data_from_db(self):
        ***REMOVED*** To get courses data from the DataBase***REMOVED***
        return self.database.courses.find({"Main_Data": True})

    def get_all_slug_and_names_of_courses_from_db(self):
        ***REMOVED*** To get all accesses (slugs - name courses) data from the DataBase***REMOVED***
        courses = []
        for course in Database().get_all_courses_data_from_db():
            courses.append({"Slug": course["Slug"], "Name": course["Name"]})
        return courses

    def get_courses_data_from_db(self, slug):
        ***REMOVED*** To get courses data from the DataBase***REMOVED***
        if self.database.courses.find_one({"Slug": slug, "Main_Data": True}) is None:
            return False

        return self.database.courses.find_one({"Slug": slug, "Main_Data": True})

    def get_days_data_of_courses_data_from_db(self, slug):
        ***REMOVED*** To get courses data from the DataBase***REMOVED***
        course_data = self.database.courses.find_one({"Slug": slug, "Main_Data": True})
        if course_data is None:
            return False

        days_data = []

        if self.database.courses.find_one({"Slug": slug, "Sub_Course": True}) is None:
            return False
        for day in self.database.courses.find({"Slug": slug, "Sub_Course": True}).sort(
            "Day"
        ):
            days_data.append(day)

        return days_data

    def get_one_day_data_of_courses_data_from_db(self, slug, day):
        ***REMOVED*** To get courses data from the DataBase***REMOVED***
        if self.database.courses.find_one({"Slug": slug, "Main_Data": True}) is None:
            return False

        try:
            int(day)
        except ValueError:
            return False

        if self.database.courses.find_one({"Slug": slug, "Sub_Course": True}) is None:
            return False
        if (
            self.database.courses.find_one(
                {"Slug": slug, "Sub_Course": True, "Day": int(day)}
            )
            is None
        ):
            return False
        return self.database.courses.find_one(
            {"Slug": slug, "Sub_Course": True, "Day": int(day)}
        )

    def get_course_info_intro_data_from_db(self, slug):
        ***REMOVED*** To get course info (intro) data from the DataBase***REMOVED***
        if self.database.courses.find_one({"Slug": slug, "Main_Data": True}) is None:
            return False

        course_data = self.database.courses.find_one({"Slug": slug, "Main_Data": True})
        try:
            intro = course_data["Intro"]
        except:
            return False

        if course_data is None or course_data == "" or course_data == []:
            return False
        else:
            return intro

    def add_users_data_to_db(
        self,
        email,
        password,
        first_name,
        last_name,
        phone_number="",
        about_me="",
        bio="",
        website="",
        birth_day="",
        birth_month="",
        birth_year="",
        Accesses=dict(),
    ):
        ***REMOVED*** To add users data to the DataBase***REMOVED***
        message = False
        if General().valid_email(email) is False:
            message = "فرمت ایمیل صحیح نمیباشد."
        elif (
            self.database.users.find_one(
                {"Email": General().corect_form_of_email(email)}
            )
            is not None
        ):
            message = "ایمیل قبلا ثبت شده است."
        elif password is None:
            message = "پسوورد را وارد کنید."
        elif len(password) <= 8:
            message = "پسوورد باید حداقل 8 کاراکتر باشد."

        if (birth_day is not None and birth_day != "") and message is False:
            try:
                birth_day = int(birth_day)
                if int(birth_day) > 31 or int(birth_day) < 0:
                    message = "روز تولد را صحیح وارد کنید."

            except:
                message = "روز تولد باید عدد باشد."

        if (birth_month is not None and birth_month != "") and message is False:
            try:
                birth_month = int(birth_month)
                if int(birth_month) > 12 or int(birth_month) < 0:
                    message = "ماه تولد را صحیح وارد کنید."

            except:
                message = "ماه تولد باید عدد باشد."

        if (birth_year is not None and birth_year != "") and message is False:
            try:
                birth_year = int(birth_year)
                if int(birth_year) > 1400 or int(birth_year) < 1200:
                    message = "سال تولد را صحیح وارد کنید."

            except:
                message = "سال تولد باید عدد باشد."

        if message is not False:
            return {"Result": False, "Message": message}

        self.database.users.insert_one(
            {
                "Email": General().corect_form_of_email(email),
                "Password": password,
                "First_Name": first_name,
                "Last_Name": last_name,
                "Accesses": Accesses,
                "Profile_Photo": "/static//assets/images/users/avatars/{}.png".format(
                    random.randint(1, 30)
                ),
            }
        )
        for key, value in {
            "Phone_Number": phone_number,
            "About_Me": about_me,
            "Bio": bio,
            "WebSite": website,
            "Birth_day": birth_day,
            "Birth_month": birth_month,
            "Birth_Year": birth_year,
        }.items():
            if value is not None and value != "":
                new_values = {"$set": {key: value}}
                self.database.users.update_one(
                    {"Email": General().corect_form_of_email(email)}, new_values
                )

        return True

    def add_users_access_data_to_db(self, email, course_name):
        ***REMOVED*** To add users accesses to the DataBase***REMOVED***
        user_data = accesses = self.database.users.find_one(
            {"Email": General().corect_form_of_email(email)}
        )
        if user_data is None:
            return False

        if "Accesses" in user_data and user_data["Accesses"] is not None:
            accesses = user_data["Accesses"]
            if isinstance(accesses, list) is False:
                accesses = dict()
        else:
            accesses = dict()

        if course_name in accesses:
            return False
        accesses[course_name] = General().days_passed_till_now()
        my_query = {"Email": General().corect_form_of_email(email)}
        new_values = {"$set": {"Accesses": accesses}}
        self.database.users.update_one(my_query, new_values)

        return True

    def add_course_data_to_db(
        self,
        name,
        slug,
        description,
        intro,
        image_href,
        now_price,
        length_of_course,
        old_price="",
        robbin="",
        published_date="",
        free=False,
        soon=False,
    ):
        ***REMOVED*** To add courses data to the DataBase***REMOVED***

        if (
            self.database.courses.find_one({"Slug": slug, "Main_Data": True})
            is not None
        ):
            return {"Result": False, "Message": "نام انگلیسی دوره وجود دارد."}

        if (free is not False and free is not True) or (
            soon is not False and soon is not True
        ):
            return {
                "Result": False,
                "Message": "مشکلی در ساختار بعضی پارامترا پیش اومده.",
            }

        if (
            slug == ""
            or name == ""
            or description == ""
            or image_href == ""
            or now_price == ""
            or length_of_course == ""
        ):
            return {"Result": False, "Message": "تمامی موارد را وارد کنید."}

        self.database.courses.insert_one(
            {
                "Main_Data": True,
                "Slug": slug,
                "Name": name,
                "Description": description,
                "Cover": image_href,
                "Old_Price": old_price,
                "Now_Price": now_price,
                "Published_Date": int(published_date),
                "Length": length_of_course,
                "Free": free,
                "Soon": soon,
            }
        )
        for key, value in {
            "Intro": intro,
            "Robbin": robbin,
        }.items():
            if value is not None and value != "":
                new_values = {"$set": {key: value}}
                self.database.courses.update_one(
                    {"Slug": slug, "Main_Data": True}, new_values
                )

        return True


    def get_payment_data(self,payment_id):
        ***REMOVED*** To get a payment data based on id from the DataBase***REMOVED***
        return self.database.payments.find_one({"ID": payment_id})


    def add_payment_record_to_db(self,slug,price,buyer_email,payment_id):
        ***REMOVED*** To add a payment record to the DataBase***REMOVED***
        self.database.payments.insert_one(
            {"Slug": slug, "Buyer": buyer_email,"Price":price , "ID": payment_id,"Status":"Waiting"}
        )
        return True


    def change_payment_status_to_success_in_db(self,payment_id):
        ***REMOVED*** To change a payment status to Successful in the DataBase***REMOVED***
        self.database.payments.update_one({"ID": payment_id}, {"$set": {"Status":"Successful"}})
        return True

    def change_payment_status_to_fail_in_db(self,payment_id):
        ***REMOVED*** To change a payment status to Failed in the DataBase***REMOVED***
        self.database.payments.update_one({"ID": payment_id}, {"$set": {"Status":"Failed"}})
        return True


    def delete_payment_record_from_db(self, payment_id):
        ***REMOVED*** To add courses data to the DataBase***REMOVED***
        my_query = {"ID": payment_id}
        try:
            self.database.payments.delete_many(my_query)
        except:
            pass
        return True


    def add_course_info_to_db(
        self, slug, introduction, speciality, importance, why, length, price, last_words
    ):
        ***REMOVED*** To add courses info data from the DataBase***REMOVED***

        if slug is None or slug == "":
            return {"Result": False, "Message": "دوره را انتخاب کنید."}

        my_query = {"Main_Data": True, "Slug": slug}
        if self.database.courses.find_one(my_query) is None:
            return {"Result": False, "Message": "دوره وجود ندارد."}

        intro = {
            "introduction": introduction,
            "speciality": speciality,
            "importance": importance,
            "why": why,
            "length": length,
            "price": price,
            "last_words": last_words,
        }
        for key, value in intro.items():
            if value is None or value == "":
                return {"Result": False, "Message": "فیلد ها نمیتوانند خالی باشند"}

        for key, value in {
            "Intro": intro,
        }.items():
            if value is not None and value != "":
                new_values = {"$set": {key: value}}
                self.database.courses.update_one(my_query, new_values)
        return True

    def add_day_of_course_data_to_db(
        self,
        slug,
        name,
        day_num,
        text,
        to_do,
        image_href,
        description,
        musics: list,
        musics_description,
        ted_video,
        ted_video_description,
        animation,
        animation_description,
        quote: list,
        movie_text,
        movie_cover,
        movie_href: dict,
        podcast,
        podcast_description,
        free: bool,
    ):
        ***REMOVED*** To add day of course data to the DataBase***REMOVED***
        try:
            int(day_num)
        except ValueError:
            return False
        if (
            self.database.courses.find_one(
                {
                    "Slug": slug,
                    "Sub_Course": True,
                    "Day": int(day_num),
                }
            )
            is not None
            or (free is not False and free is not True)
        ):
            return False

        self.database.courses.insert_one(
            {
                "Sub_Course": True,
                "Slug": slug,
                "Name": name,
                "Day": int(day_num),
                "Cover": image_href,
                "Description": description,
                "Text": text,
                "To_Do": to_do,
                "Quotes": quote,
                "Musics": musics,
                "Musics_Description": musics_description,
                "Ted_Video": ted_video,
                "Ted_Video_Description": ted_video_description,
                "Animation_Link": animation,
                "Animation_Description": animation_description,
                "Movie_Links": movie_href,
                "Movie_Text": movie_text,
                "Movie_Cover": movie_cover,
                "Podcast": podcast,
                "Podcast_Description": podcast_description,
                "Free": free,
            }
        )
        return True

    def create_a_none_day_of_course_data_in_db(self, course_name_slug, day_num):
        ***REMOVED*** To create a none-data day of course in the DataBase***REMOVED***
        try:
            int(day_num)
        except ValueError:
            return {"Result": False, "Message": "روز وارد شده عدد نمیباشد."}

        if (
            self.database.courses.find_one(
                {
                    "Slug": course_name_slug,
                    "Sub_Course": True,
                    "Day": int(day_num),
                }
            )
            is not None
        ):
            return {"Result": False, "Message": "روز دوره وجود دارد."}

        self.database.courses.insert_one(
            {
                "Sub_Course": True,
                "Slug": course_name_slug,
                "Name": None,
                "Day": int(day_num),
                "Cover": None,
                "Description": None,
                "Text": None,
                "To_Do": None,
                "Quotes": None,
                "Musics": None,
                "Musics_Description": None,
                "Ted_Video": None,
                "Ted_Video_Description": None,
                "Animation_Link": None,
                "Animation_Description": None,
                "Movie_Links": None,
                "Movie_Text": None,
                "Movie_Cover": None,
                "Podcast": None,
                "Podcast_Description": None,
                "Free": None,
            }
        )
        return True

    def add_day_essential_data_to_db(
        self, course_name_slug, day_num, name_persian, description, image_path, freeness
    ):
        ***REMOVED*** To add essential data to a day of course in the DataBase***REMOVED***
        try:
            int(day_num)
        except ValueError:
            return {"Result": False, "Message": "روز وارد شده عدد نمیباشد."}

        overwrite = False
        if (
            self.database.courses.find_one(
                {
                    "Slug": course_name_slug,
                    "Sub_Course": True,
                    "Day": int(day_num),
                }
            )
            is None
        ):
            Database().create_a_none_day_of_course_data_in_db(course_name_slug, day_num)
        # varrivle , if overwrite or not
        else:
            day_data = Database().get_one_day_data_of_courses_data_from_db(
                course_name_slug, day_num
            )
            if (
                day_data["Name"] is not None
                or day_data["Cover"] is not None
                or day_data["Description"] is not None
            ):
                overwrite = True

        response_edit_of_day = Database().edit_day_of_course_data_to_db(
            slug=course_name_slug,
            day_of_course=day_num,
            name_of_day=name_persian,
            description=description,
            image_href=image_path,
            free=freeness,
        )
        print(response_edit_of_day)
        if response_edit_of_day is False:
            return {"Result": False, "Message": "مشکلاتی در دیتابیس به وجود امده است."}

        if overwrite is True:
            return {
                "Result": True,
                "Message": "تغییرات با موفقیت انجام شد. دیتاها رونویسی شدند.",
            }

        return True

    def add_day_text_data_to_db(self, course_name_slug, day_num, text):
        ***REMOVED*** To add main text to a day of course in the DataBase***REMOVED***
        try:
            int(day_num)
        except ValueError:
            return {"Result": False, "Message": "روز وارد شده عدد نمیباشد."}

        overwrite = False
        if (
            self.database.courses.find_one(
                {
                    "Slug": course_name_slug,
                    "Sub_Course": True,
                    "Day": int(day_num),
                }
            )
            is None
        ):
            Database().create_a_none_day_of_course_data_in_db(course_name_slug, day_num)
        # varrivle , if overwrite or not
        else:
            day_data = Database().get_one_day_data_of_courses_data_from_db(
                course_name_slug, day_num
            )
            if day_data["Text"] is not None:
                overwrite = True

        response_edit_of_day = Database().edit_day_of_course_data_to_db(
            slug=course_name_slug, day_of_course=day_num, text=text
        )
        if response_edit_of_day is False:
            return {"Result": False, "Message": "مشکلاتی در دیتابیس به وجود امده است."}

        if overwrite is True:
            return {
                "Result": True,
                "Message": "تغییرات با موفقیت انجام شد. دیتاها رونویسی شدند.",
            }

        return True

    def add_day_todo_data_to_db(self, course_name_slug, day_num, todo):
        ***REMOVED*** To add essential data to a day of course in the DataBase***REMOVED***
        try:
            int(day_num)
        except ValueError:
            return {"Result": False, "Message": "روز وارد شده عدد نمیباشد."}

        overwrite = False
        if (
            self.database.courses.find_one(
                {
                    "Slug": course_name_slug,
                    "Sub_Course": True,
                    "Day": int(day_num),
                }
            )
            is None
        ):
            Database().create_a_none_day_of_course_data_in_db(course_name_slug, day_num)
        # varrivle , if overwrite or not
        else:
            day_data = Database().get_one_day_data_of_courses_data_from_db(
                course_name_slug, day_num
            )
            if day_data["To_Do"] is not None:
                overwrite = True

        response_edit_of_day = Database().edit_day_of_course_data_to_db(
            slug=course_name_slug, day_of_course=day_num, to_do=todo
        )
        if response_edit_of_day is False:
            return {"Result": False, "Message": "مشکلاتی در دیتابیس به وجود امده است."}

        if overwrite is True:
            return {
                "Result": True,
                "Message": "تغییرات با موفقیت انجام شد. دیتاها رونویسی شدند.",
            }

        return True

    def add_day_quotes_data_to_db(self, course_name_slug, day_num, quotes):
        ***REMOVED*** To add quotes data to a day of course in the DataBase***REMOVED***
        try:
            int(day_num)
        except ValueError:
            return {"Result": False, "Message": "روز وارد شده عدد نمیباشد."}

        overwrite = False
        if (
            self.database.courses.find_one(
                {
                    "Slug": course_name_slug,
                    "Sub_Course": True,
                    "Day": int(day_num),
                }
            )
            is None
        ):
            Database().create_a_none_day_of_course_data_in_db(course_name_slug, day_num)
        # varrivle , if overwrite or not
        else:
            day_data = Database().get_one_day_data_of_courses_data_from_db(
                course_name_slug, day_num
            )
            if day_data["Quotes"] is not None and day_data["Quotes"] != []:
                overwrite = True

        response_edit_of_day = Database().edit_day_of_course_data_to_db(
            slug=course_name_slug, day_of_course=day_num, quote=quotes
        )
        if response_edit_of_day is False:
            return {"Result": False, "Message": "مشکلاتی در دیتابیس به وجود امده است."}

        if overwrite is True:
            return {
                "Result": True,
                "Message": "تغییرات با موفقیت انجام شد. دیتاها رونویسی شدند.",
            }

        return True

    def add_day_musics_data_to_db(
        self, course_name_slug, day_num, description, covers, musics, creators, names
    ):
        ***REMOVED*** To add musics data to a day of course in the DataBase***REMOVED***
        try:
            int(day_num)
        except ValueError:
            return {"Result": False, "Message": "روز وارد شده عدد نمیباشد."}

        overwrite = False
        if (
            self.database.courses.find_one(
                {
                    "Slug": course_name_slug,
                    "Sub_Course": True,
                    "Day": int(day_num),
                }
            )
            is None
        ):
            print(
                Database().create_a_none_day_of_course_data_in_db(
                    course_name_slug, day_num
                )
            )
        # varrivle , if overwrite or not
        else:
            day_data = Database().get_one_day_data_of_courses_data_from_db(
                course_name_slug, day_num
            )
            if (
                day_data["Musics"] is not None and day_data["Musics"] != []
            ) or day_data["Musics_Description"] is not None:
                overwrite = True

        if not (
            len(covers) == len(musics)
            and len(covers) == len(creators)
            and len(covers) == len(names)
        ):
            return {
                "Result": False,
                "Message": "همه اطلاعات رو وارد کنید و فیلدی رو خالی نزارید.",
            }

        musics_data = []
        for index in range(len(musics)):
            music = musics[index]
            cover = covers[index]
            name = names[index]
            creator = creators[index]
            music_path = General().save_music_of_day(course_name_slug, day_num, music)
            image_path = General().save_music_cover_of_day(cover_bytes=cover.read())
            musics_data.append(
                {
                    "name": name,
                    "artist": creator,
                    "cover": image_path["href"],
                    "url": music_path["href"],
                    "theme": "#ebd0c2",
                }
            )

        response_edit_of_day = Database().edit_day_of_course_data_to_db(
            slug=course_name_slug,
            day_of_course=day_num,
            musics=musics_data,
            musics_description=description,
        )

        if response_edit_of_day is False:
            return {"Result": False, "Message": "مشکلاتی در دیتابیس به وجود امده است."}

        if overwrite is True:
            return {
                "Result": True,
                "Message": "تغییرات با موفقیت انجام شد. دیتاها رونویسی شدند.",
            }

        return True

    def add_day_ted_data_to_db(
        self, course_name_slug, day_num, description, urls, qualities
    ):
        ***REMOVED*** To add ted videos data to a day of course in the DataBase***REMOVED***
        try:
            int(day_num)
        except ValueError:
            return {"Result": False, "Message": "روز وارد شده عدد نمیباشد."}

        overwrite = False
        if (
            self.database.courses.find_one(
                {
                    "Slug": course_name_slug,
                    "Sub_Course": True,
                    "Day": int(day_num),
                }
            )
            is None
        ):
            print(
                Database().create_a_none_day_of_course_data_in_db(
                    course_name_slug, day_num
                )
            )
        # varrivle , if overwrite or not
        else:
            day_data = Database().get_one_day_data_of_courses_data_from_db(
                course_name_slug, day_num
            )
            if (
                day_data["Ted_Video"] is not None and day_data["Ted_Video"] != []
            ) or day_data["Ted_Video_Description"] is not None:
                overwrite = True

        if not (len(urls) == len(qualities)):
            return {
                "Result": False,
                "Message": "همه اطلاعات رو وارد کنید و فیلدی رو خالی نزارید.",
            }

        teds_data = []
        for index in range(len(urls)):
            url = urls[index]
            quality = qualities[index]
            teds_data.append(
                {
                    "Link": url,
                    "Quality": quality,
                }
            )

        response_edit_of_day = Database().edit_day_of_course_data_to_db(
            slug=course_name_slug,
            day_of_course=day_num,
            ted_video=teds_data,
            ted_video_description=description,
        )

        if response_edit_of_day is False:
            return {"Result": False, "Message": "مشکلاتی در دیتابیس به وجود امده است."}

        if overwrite is True:
            return {
                "Result": True,
                "Message": "تغییرات با موفقیت انجام شد. دیتاها رونویسی شدند.",
            }

        return True

    def add_day_animation_data_to_db(
        self, course_name_slug, day_num, description, urls, qualities
    ):
        ***REMOVED*** To add short film animation data to a day of course in the DataBase***REMOVED***
        try:
            int(day_num)
        except ValueError:
            return {"Result": False, "Message": "روز وارد شده عدد نمیباشد."}

        overwrite = False
        if (
            self.database.courses.find_one(
                {
                    "Slug": course_name_slug,
                    "Sub_Course": True,
                    "Day": int(day_num),
                }
            )
            is None
        ):
            print(
                Database().create_a_none_day_of_course_data_in_db(
                    course_name_slug, day_num
                )
            )
        # varrivle , if overwrite or not
        else:
            day_data = Database().get_one_day_data_of_courses_data_from_db(
                course_name_slug, day_num
            )
            if (
                day_data["Animation_Link"] is not None
                and day_data["Animation_Link"] != []
            ) or day_data["Animation_Description"] is not None:
                overwrite = True

        if not (len(urls) == len(qualities)):
            return {
                "Result": False,
                "Message": "همه اطلاعات رو وارد کنید و فیلدی رو خالی نزارید.",
            }

        teds_data = []
        for index in range(len(urls)):
            url = urls[index]
            quality = qualities[index]
            teds_data.append(
                {
                    "Link": url,
                    "Quality": quality,
                }
            )

        response_edit_of_day = Database().edit_day_of_course_data_to_db(
            slug=course_name_slug,
            day_of_course=day_num,
            animation=teds_data,
            animation_description=description,
        )

        if response_edit_of_day is False:
            return {"Result": False, "Message": "مشکلاتی در دیتابیس به وجود امده است."}

        if overwrite is True:
            return {
                "Result": True,
                "Message": "تغییرات با موفقیت انجام شد. دیتاها رونویسی شدند.",
            }

        return True

    def add_day_podcast_data_to_db(
        self, course_name_slug, day_num, description, url, name, creator, cover
    ):
        ***REMOVED*** To add podcast data to a day of course in the DataBase***REMOVED***
        try:
            int(day_num)
        except ValueError:
            return {"Result": False, "Message": "روز وارد شده عدد نمیباشد."}

        overwrite = False
        if (
            self.database.courses.find_one(
                {
                    "Slug": course_name_slug,
                    "Sub_Course": True,
                    "Day": int(day_num),
                }
            )
            is None
        ):
            print(
                Database().create_a_none_day_of_course_data_in_db(
                    course_name_slug, day_num
                )
            )
        # varrivle , if overwrite or not
        else:
            day_data = Database().get_one_day_data_of_courses_data_from_db(
                course_name_slug, day_num
            )
            if (
                day_data["Podcast"] is not None and day_data["Podcast"] != []
            ) or day_data["Podcast_Description"] is not None:
                overwrite = True

        if url == "" or creator == "" or name == "":
            return {
                "Result": False,
                "Message": "همه اطلاعات رو وارد کنید و فیلدی رو خالی نزارید.",
            }

        podcast_cover_path = General().save_podcast_cover_of_day(
            cover_bytes=cover.read()
        )

        podcast_data = {
            "name": name,
            "artist": creator,
            "url": url,
            "cover": podcast_cover_path["href"],
        }
        response_edit_of_day = Database().edit_day_of_course_data_to_db(
            slug=course_name_slug,
            day_of_course=day_num,
            podcast=podcast_data,
            podcast_description=description,
        )

        if response_edit_of_day is False:
            return {"Result": False, "Message": "مشکلاتی در دیتابیس به وجود امده است."}

        if overwrite is True:
            return {
                "Result": True,
                "Message": "تغییرات با موفقیت انجام شد. دیتاها رونویسی شدند.",
            }

        return True

    def add_day_movie_data_to_db(
        self, course_name_slug, day_num, description, urls, qualities, cover
    ):
        ***REMOVED*** To add movie data to a day of course in the DataBase***REMOVED***
        try:
            int(day_num)
        except ValueError:
            return {"Result": False, "Message": "روز وارد شده عدد نمیباشد."}

        overwrite = False
        if (
            self.database.courses.find_one(
                {
                    "Slug": course_name_slug,
                    "Sub_Course": True,
                    "Day": int(day_num),
                }
            )
            is None
        ):
            print(
                Database().create_a_none_day_of_course_data_in_db(
                    course_name_slug, day_num
                )
            )

        else:
            day_data = Database().get_one_day_data_of_courses_data_from_db(
                course_name_slug, day_num
            )
            if (
                (day_data["Movie_Links"] is not None and day_data["Movie_Links"] != [])
                or day_data["Movie_Text"] is not None
                or day_data["Movie_Cover"] is not None
            ):
                overwrite = True

        if not (len(urls) == len(qualities)):
            return {
                "Result": False,
                "Message": "همه اطلاعات رو وارد کنید و فیلدی رو خالی نزارید.",
            }

        uploaded_image_bytes = cover.read()

        hash_image = General().sha256_hash_bytes(uploaded_image_bytes)

        format_file = General().format_recognizer(uploaded_image_bytes)
        file_name = "movie_picture_of_course_" + str(hash_image) + "." + format_file
        location_image = "static/assets/images/days_of_course/" + file_name
        location_image_href = "/static//assets/images/days_of_course/" + file_name
        with open(location_image, "wb") as file:
            file.write(uploaded_image_bytes)
        General().image_resizer_using_imgp(location_image, 600)
        General().image_optimizer_using_imgp(location_image)

        movie_data = []
        for index in range(len(urls)):
            url = urls[index]
            quality = qualities[index]
            movie_data.append(
                {
                    "Link": url,
                    "Quality": quality,
                }
            )

        response_edit_of_day = Database().edit_day_of_course_data_to_db(
            slug=course_name_slug,
            day_of_course=day_num,
            movie_href=movie_data,
            movie_cover=location_image_href,
            movie_text=description,
        )
        if response_edit_of_day is False:
            return {"Result": False, "Message": "مشکلاتی در دیتابیس به وجود امده است."}

        if overwrite is True:
            return {
                "Result": True,
                "Message": "تغییرات با موفقیت انجام شد. دیتاها رونویسی شدند.",
            }

        return True

    def edit_users_data_from_db(
        self,
        old_email,
        first_name="",
        last_name="",
        phone_number="",
        about_me="",
        bio="",
        website="",
        birth_day="",
        birth_month="",
        birth_year="",
        new_password="",
    ):
        ***REMOVED*** To edit users data from the DataBase***REMOVED***
        if (
            self.database.users.find_one(
                {"Email": General().corect_form_of_email(old_email)}
            )
            is None
        ):
            return False

        for key, value in {
            "Password": new_password,
            "First_Name": first_name,
            "Last_Name": last_name,
            "Phone_Number": phone_number,
            "About_Me": about_me,
            "Bio": bio,
            "WebSite": website,
            "Birth_day": birth_day,
            "Birth_month": birth_month,
            "Birth_Year": birth_year,
        }.items():
            if value is not None and value != "":
                new_values = {"$set": {key: value}}
                self.database.users.update_one(
                    {"Email": General().corect_form_of_email(old_email)}, new_values
                )

        return True

    def edit_courses_data_from_db(
        self,
        slug,
        name="",
        intro="",
        description="",
        image_href="",
        price="",
        length_of_course="",
        free="",
    ):
        ***REMOVED*** To edit courses data from the DataBase***REMOVED***

        my_query = {"Main_Data": True, "Slug": slug}
        if self.database.courses.find_one(my_query) is not None or (
            free is not False or free is not True
        ):
            return False

        for key, value in {
            "Slug": slug,
            "Name": name,
            "Description": description,
            "Intro": intro,
            "Cover": image_href,
            "Price": price,
            "Length": length_of_course,
            "Free": free,
        }.items():
            if value is not None and value != "":
                new_values = {"$set": {key: value}}
                self.database.courses.update_one(my_query, new_values)
        return True

    def edit_day_of_course_data_to_db(
        self,
        slug,
        day_of_course,
        name_of_day="",
        day_num="",
        text="",
        to_do="",
        image_href="",
        description="",
        musics: list = "",
        musics_description="",
        ted_video="",
        ted_video_description="",
        animation="",
        animation_description="",
        quote: list = "",
        movie_text="",
        movie_cover="",
        movie_href: dict = "",
        podcast="",
        podcast_description="",
        free: bool = "",
    ):
        ***REMOVED*** To edit day data from the DataBase***REMOVED***
        try:
            if day_num != "":
                day_num = int(day_num)
            int(day_of_course)
        except ValueError:
            return False

        my_query = {
            "Day": int(day_of_course),
            "Slug": slug,
            "Sub_Course": True,
        }
        if self.database.courses.find_one(my_query) is None or not (
            free is False or free is True or free == ""
        ):
            print("here----------")
            return False

        for key, value in {
            "Name": name_of_day,
            "Day": day_num,
            "Cover": image_href,
            "Description": description,
            "Text": text,
            "To_Do": to_do,
            "Quotes": quote,
            "Musics": musics,
            "Musics_Description": musics_description,
            "Ted_Video": ted_video,
            "Ted_Video_Description": ted_video_description,
            "Animation_Link": animation,
            "Animation_Description": animation_description,
            "Movie_Links": movie_href,
            "Movie_Text": movie_text,
            "Movie_Cover": movie_cover,
            "Podcast": podcast,
            "Podcast_Description": podcast_description,
            "Free": free,
        }.items():
            if value is not None and value != "":
                new_values = {"$set": {key: value}}
                self.database.courses.update_one(my_query, new_values)
        return True

    def delete_parts_of_day_of_course_data_in_db(
        self, slug, day_of_course, remove_parts_names: list
    ):
        ***REMOVED*** To remove specific parts of day data from the DataBase***REMOVED***
        try:
            int(day_of_course)
        except ValueError:
            return False

        my_query = {
            "Day": int(day_of_course),
            "Slug": slug,
            "Sub_Course": True,
        }

        for key in remove_parts_names:
            if key is not None and key != "":
                new_values = {"$set": {key: None}}
                self.database.courses.update_one(my_query, new_values)
        return True

    def delete_users_data_from_db(self, email):
        ***REMOVED*** To delete users data from the DataBase***REMOVED***
        if (
            self.database.users.find_one(
                {"Email": General().corect_form_of_email(email)}
            )
            is None
        ):
            return False
        self.database.users.delete_one({"Email": General().corect_form_of_email(email)})
        return True

    def delete_courses_data_from_db(self, slug):
        ***REMOVED*** To delete courses data from the DataBase***REMOVED***
        my_query = {"Slug": slug}
        if self.database.courses.find_one(my_query) is None:
            return False

        self.database.courses.delete_many({"Slug": slug})
        return True

    def delete_day_of_course_data_to_db(self, slug, day):
        ***REMOVED*** To add courses data to the DataBase***REMOVED***
        try:
            int(day)
        except ValueError:
            return {"Result": False, "Message": "روز وارد شده عدد نمیباشد."}
        my_query = {"Slug": slug, "Day": int(day), "Sub_Course": True}
        if self.database.courses.find_one(my_query) is None:
            return {"Result": False, "Message": "همچین روزی وجود ندارد."}

        self.database.courses.delete_many(my_query)
        return True


class PageDetails:
    ***REMOVED*** All functions related to the pages details input ! ***REMOVED***

    def __init__(self, session=None):
        ***REMOVED*** Get session to be used in some of the functions for the page details. ***REMOVED***
        self.session = session

    def index_data(self):
        ***REMOVED*** To return all details that are needed at index page. ***REMOVED***
        try:
            email = self.session["Data"]["Email"]
        except:
            email = False
        if email is not False:
            signed_in_email_data = Database().get_users_data_from_db(
                General().corect_form_of_email(email)
            )
        else:
            signed_in_email_data = False
        if (
            email is False
            or signed_in_email_data is False
            or Authentication(self.session).is_signed_in() is False
        ):
            return {
                "First_Name": "ناشناس",
                "Last_Name": "",
                "Profile_Photo": "/static//assets/images/users/avatars/4.png",
                "User": False,
            }

        del signed_in_email_data["Password"]
        signed_in_email_data["User"] = True
        return signed_in_email_data

    def all_courses_page_info_html(self):
        ***REMOVED*** To return all details that are needed at /Courses page. ***REMOVED***
        courses_raw = Database().get_all_courses_data_from_db()
        courses = list()
        for course in courses_raw:
            courses.append(course)

        return courses

    def info_intro_course_page(self, slug):
        ***REMOVED*** To return all details that are needed at /Course/<slug>/info page. ***REMOVED***
        course = Database().get_courses_data_from_db(slug)
        return course

    def course_page_info(self, slug):
        ***REMOVED*** To return all details that are needed at /Course/<slug> page. ***REMOVED***
        days_raw = Database().get_days_data_of_courses_data_from_db(slug)
        course = Database().get_courses_data_from_db(slug)
        days = list()
        if course is False:
            return False

        if days_raw is False:
            days_raw = []

        intro = True
        if Database().get_course_info_intro_data_from_db(slug) is False:
            intro = False

        for day in days_raw:
            days.append(day)

        return [course, days, intro]

    def sub_course_page_info_html(self, slug, day):
        ***REMOVED*** To return all details that are needed at /Course/<course> page. ( Day data ) ***REMOVED***
        day = Database().get_one_day_data_of_courses_data_from_db(slug, day)
        return day

    def day_of_the_course(self):
        ***REMOVED*** To delete courses data from the DataBase. ***REMOVED***

    def all_day_parts_to_remove_in_admin_page(self):
        parts_raw = [
            {"Slug": "Name", "Name": "اسم روز"},
            {"Slug": "Cover", "Name": "کاور روز"},
            {"Slug": "Description", "Name": "توضیحات روز"},
            {"Slug": "Text", "Name": "متن اصلی روز"},
            {"Slug": "To_Do", "Name": "تمارین روز"},
            {"Slug": "Quotes", "Name": "نقل قول های روز"},
            {"Slug": "Musics", "Name": "موزیک های روز"},
            {"Slug": "Musics_Description", "Name": "توضیحات موزیک های  روز"},
            {"Slug": "Ted_Video", "Name": "ویدیو تد روز"},
            {"Slug": "Ted_Video_Description", "Name": "توضیحات ویدیو تد روز"},
            {"Slug": "Animation_Link", "Name": "لینک های انیمیشن کوتاه روز"},
            {"Slug": "Animation_Description", "Name": "توضیحات انیمیشن کوتاه روز"},
            {"Slug": "Movie_Links", "Name": "لینک فیلم های روز"},
            {"Slug": "Movie_Text", "Name": "متن و توضیحات فیلم روز"},
            {"Slug": "Movie_Cover", "Name": "کاور فیلم روز"},
            {"Slug": "Podcast", "Name": "پادکست پیشنهادی روز"},
            {"Slug": "Podcast_Description", "Name": "توضیحات پادکست روز"},
        ]

        length_parts = len(parts_raw)
        parts = [
            parts_raw[0 : ceil(length_parts / 3)],
            parts_raw[ceil(length_parts / 3) : (ceil(length_parts / 3)) * 2],
            parts_raw[(ceil(length_parts / 3)) * 2 :],
        ]
        return parts
    
    def all_course_data_slug_name_to_remove_in_admin_page(self):
        parts_raw = []
        for course in PageDetails().all_courses_page_info_html():
            parts_raw.append({"Slug":course["Slug"],"Name":course["Name"]})
            
        length_parts = len(parts_raw)
        parts = [
            parts_raw[0 : ceil(length_parts / 3)],
            parts_raw[ceil(length_parts / 3) : (ceil(length_parts / 3)) * 2],
            parts_raw[(ceil(length_parts / 3)) * 2 :],
        ]
        return parts


    def all_accesses_admin_page(self):
        accesses_raw = Database().get_all_slug_and_names_of_courses_from_db()
        length_accesses = len(accesses_raw)
        accesses = [
            accesses_raw[0 : ceil(length_accesses / 3)],
            accesses_raw[ceil(length_accesses / 3) : (ceil(length_accesses / 3)) * 2],
            accesses_raw[(ceil(length_accesses / 3)) * 2 :],
        ]
        return accesses

    def get_all_courses_info_categorized_by_info_existence(self):
        ***REMOVED*** To get all courses (slugs - name courses) data plus being categorized ***REMOVED***
        courses_categorized = {"دوره ها": [], "دوره های همراه با اینفو": []}
        for course in Database().get_all_courses_data_from_db():
            if "info" not in course or course["info"] == []:
                courses_categorized["دوره ها"].append(
                    {"Slug": course["Slug"], "Name": course["Name"]}
                )
            else:
                courses_categorized["دوره های همراه با اینفو"].append(
                    {"Slug": course["Slug"], "Name": course["Name"]}
                )
        return courses_categorized

    def motivation_wall_page_info_html(self):
        ***REMOVED*** To return all details that are needed at /MotivationWall page. ***REMOVED***

    def profile_page_info_html(self):
        ***REMOVED*** To return all details that are needed at /Profile page. ***REMOVED***

    def mail_page_info_html(self):
        ***REMOVED*** To return all details that are needed at /Profile page. ***REMOVED***

    def number_of_courses(self):
        ***REMOVED*** To return count of courses that is needed at / page. ***REMOVED***
        return Database().get_all_courses_data_from_db().count()
        
    def top_3_expensive_courses(self):
        ***REMOVED*** To return top 3 courses that are needed at / page. ***REMOVED***
        courses = [] #.sort("Now_Price")
        for course in Database().get_all_courses_data_from_db():
            course["Now_Price"] = int(str(course["Now_Price"]).replace(',', ''))
            if General().days_passed_till_now() >= course["Published_Date"]:
                courses.append(course)
        courses = sorted(courses, key=lambda k: k['Now_Price'])
        courses.reverse()
        return courses[0:2]
        
    def random_quotes(self,count=3):
        quotes = ['به تنهایی نمی‌توانم دنیا را تغییر بدهم اما می‌توانم سنگی را به آب بیندازم تا موج‌های بسیار خلق کند.',
        'یگانه فردی که سرنوشت از شما خواهد ساخت همانی است که خودتان تصمیم می‌گیرید باشید.',
        'رؤیاهای‌ خودتان را بسازید در غیر این صورت فرد دیگری شما را برای ساختن رؤیایش به کار خواهد گرفت.',
        'سؤال این نیست که چه کسی به من اجازه خواهد داد؛ بلکه این است که چه کسی قرار است جلوی من را بگیرد.',
        'اگر بهت گفتند نمی‌تونی کاری رو انجام بدی، فقط بهشون بخند! بعدا می‌فهمند که چرا بهشون خندیدی.',
        'راه حل صحیح موفقیت این است که اشتیاق شما به پیروزی بیشتر از ترس شما از شکست باشد.',
        'ما نسبت به آشکار ترین چیز ها نابینا هستیم و مشکل این جاست که نابینایی خود را هم نمی بینیم.',
        'اگر امسال درمورد پارسال تان فکر می کنید و احساس حماقت ندارید پس به اندازه کافی پیشرفت نکرده اید.',
        'نقطه مشترک تمام افراد موفق در این است که حد فاصل میان تصمیم و عمل را بسیار کوچک نگه می دارند.',
        'اگر وقت زیادی را صرف فکر کردن راجع به موضوعی کنی ، هیچ وقت آن را به انجام نخواهی رساند.',
        'شما با حفظ کردن قواعد راه رفتن را یاد نمی گیرید. بلکه با انجام دادن و زمین خوردن است که می آموزید.',
        'شما با دنبال کردن قواعد ، راه رفتن را یاد نمی گیرید. با انجام دادن و شکست خوردن است که یاد می گیرید.',
        'درد موقتیه ، فقط برای موفق شدن تحملش میکنید اما اگر تسلیم شوید ، شکست تا آخر عمرتان با شما خواهد بود.',]
        chosen_quotes=[]
        for quote_count in range (count):
            chosen_single_quote = random.choice(quotes)
            chosen_quotes.append(chosen_single_quote)
            quotes.remove(chosen_single_quote)
        return chosen_quotes
        
    def random_blog_post(self):
        r = requests.get('http://127.0.0.1:1221/').text
        #print (r)
        r = r.replace('\r','\\r').replace('\n','\\n').strip()
        #print (ast.literal_eval(r))
        
        
        pprint (json.loads(r)[0]["_links"])
        
        
        #print (r.status_code)
        #print (r.headers['content-type'])
        #print (r.encoding)
        #print (r.text)