import base64
from datetime import datetime
#
from PIL import Image
import io
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from About.models import About
from Candidate.models import Candidate
from Election.models import Election
from ElectionCandidate.models import ElectionCandidate
from Gallery.models import Gallery
from Vote.models import Vote
from Voter.models import Voter
from Voter.proctoring import FaceRecognition

'''modules for otp verification'''
from Voter.otp import OtpHandler
from django.conf import settings
from twilio.rest import Client

'''modules for face verification'''
import face_recognition
from django.http import JsonResponse, HttpResponse
import cv2
import numpy as np


def home(request):
    data = {'title': 'Home'}
    return render(request, 'home.html', data)


def about(request):
    GalleryData = Gallery.objects.all()
    AboutData1 = About.objects.all()[:2]
    AboutData2 = About.objects.all()[2:4]

    data = {'title': 'About Us', 'gallerydata': GalleryData,
            'aboutdata1': AboutData1, 'aboutdata2': AboutData2}
    return render(request, 'about.html', data)


def election(request):
    current_date = datetime.now()
    electiondata = Election.objects.all()
    data = {'title': 'Elections', 'date_time': current_date, 'electiondata': electiondata}
    return render(request, 'elections.html', data)


def contactus(request):
    data = {'title': 'Contact Us'}
    return render(request, 'contactus.html', data)


def login_user(request, eid):
    eid = eid
    data = {'title': 'Login', 'eid': eid}

    if request.method == 'POST':
        username = request.POST.get('voter')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            voter = get_object_or_404(Voter, vid=username)
            vote_exists = Vote.objects.filter(vid_id=username, eid_id=eid, casted=True).exists()
            if user is not None:

                if vote_exists:
                    alert_message = 'You have already casted your vote for this election!'
                    messages.error(request, alert_message)
                else:
                    login(request, user)
                    request.session['eid'] = eid
                    OtpHandler(voter.phone).send_otp()
                    return redirect('verify_otp')

        else:
            messages.error(request, 'Invalid login credentials')

    return render(request, 'login.html', data)


def verify_otp(request):
    voter = get_object_or_404(Voter, vid=request.user.username)

    if request.method == 'POST':
        getotp = request.POST.get('otp')

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        verification_check = client.verify.v2.services(settings.TWILIO_VERIFY_SID) \
            .verification_checks \
            .create(to='+91' + str(voter.phone), code=getotp)

        if verification_check.status == 'approved':
            login(request, request.user)
            return redirect('authentication')
        else:
            messages.error(request, 'Invalid OTP')

    data = {'title': 'OTP Verification', 'voterdata': voter}
    return render(request, 'otpverify.html', data)


def authentication(request):
    VoterData = get_object_or_404(Voter, vid=request.user.username)
    data = {'title': 'Face Verification', 'voterdata': VoterData}
    return render(request, 'authentication.html', data)


@csrf_exempt
def verify_user(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        request.session['voter_image'] = image_data
        user_photo = Voter.objects.get(vid=request.user.username).photo

        # Load the user's photo from the database and convert it to a numpy array
        user_photo_data = np.asarray(bytearray(user_photo.read()), dtype=np.uint8)
        user_photo_array = cv2.imdecode(user_photo_data, cv2.IMREAD_COLOR)

        # Decode the image data and load it as a numpy array
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        captured_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # Encode the user's photo and the captured image using face_recognition library
        user_photo_encoding = face_recognition.face_encodings(user_photo_array)[0]
        captured_image_encodings = face_recognition.face_encodings(captured_image)

        if len(captured_image_encodings) > 0:
            captured_image_encoding = captured_image_encodings[0]
            is_match = face_recognition.compare_faces([user_photo_encoding], captured_image_encoding)[0]
            if is_match:
                request.session['voter_image'] = image_data
                result = {'is_match': True}
                return JsonResponse({'is_match': str(result['is_match'])})
        else:
            return JsonResponse({'is_match': False, 'message': 'No faces were found in the captured image'})



def voting(request):
    eid = request.session.get('eid')
    voterdata = get_object_or_404(Voter, vid=request.user.username)
    candidatedata = Candidate.objects.all()
    electiondata = get_object_or_404(Election, eid=eid)
    election_candidate = ElectionCandidate.objects.all()

    data = {'title': 'Voting Panel', 'voterdata': voterdata, 'candidatedata': candidatedata,
            'election_candidate': election_candidate, 'electiondata': electiondata, 'eid': eid}

    return render(request, 'voting.html', data)

'''

@csrf_exempt
def face_proctoring(request):
    if request.method == 'POST':
        user_id = request.user.username
        voter_image = Voter.objects.get(vid=user_id).photo

        print(voter_image)
        proctored_image = request.FILES.get('image')
        print(proctored_image)

        if proctored_image:
            # fr = FaceRecognition(voter_image, user_id)
            # fr.run(proctored_image)

            # Read and decode stored image

            voter_image_data = np.asarray(bytearray(voter_image.read()), dtype=np.uint8)
            voter_image_array = cv2.imdecode(voter_image_data, cv2.IMREAD_COLOR)

            fr = FaceRecognition(voter_image, user_id)
            fr.run(proctored_image, result)

            # Read and decode uploaded image
            proctored_image_data = proctored_image.read()
            proctored_image_array = np.frombuffer(proctored_image_data, dtype=np.uint8)
            print(proctored_image_array)
            # captured_image = cv2.imdecode(proctored_image_array, cv2.IMREAD_COLOR)

            # Get face encodings
            voter_image_encoding = face_recognition.face_encodings(voter_image_array)[0]
            captured_image_encodings = face_recognition.face_encodings(proctored_image_array)

            # Compare faces
            if len(captured_image_encodings) > 0:
                captured_image_encoding = captured_image_encodings[0]
                is_match = face_recognition.compare_faces([voter_image_encoding], captured_image_encoding)[0]
                if is_match:
                    result = {'is_match': True}
                    return JsonResponse(result)
            return JsonResponse({'is_match': False})

'''


def cast_vote(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')
        eid = request.session.get('eid')
        vid = request.user.username
        # print(cid)
        #
        # if not cid:
        #     return JsonResponse({'success': None })

        # Check if the voter has already casted a vote in this election
        vote_exists = Vote.objects.filter(vid_id=vid, eid_id=eid, casted=True).exists()
        if vote_exists:
            return JsonResponse({'success': False})

        # Check if the voter has already casted a vote for this candidate in this election
        candidate_vote_exists = Vote.objects.filter(vid_id=vid, eid_id=eid, cid_id=cid, casted=True).exists()
        if candidate_vote_exists:
            return JsonResponse({'success': False})

        # Create a new vote for the candidate
        vote, created = Vote.objects.get_or_create(vid_id=vid, eid_id=eid, cid_id=cid,
                                                   defaults={'count': 1, 'casted': True})
        if not created:
            vote.count += 1
            vote.casted = True
            vote.save()

        return JsonResponse({'success': True})
    else:
        return HttpResponseNotAllowed(['POST'])


def vote_success(request):
    success = get_object_or_404(Voter, vid=request.user.username)
    data = {'title': 'Voting Successful', 'success': success}

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+12705618585',
        messaging_service_sid='MG16b24af00f819f423f1f41b17cf6b4df',
        body=f'Dear {success.name}, Thank You for casting your vote. Your vote has been recorded successfully.',
        to='+91' + str(success.phone)
    )

    return render(request, 'votesuccess.html', data)





def result(request, eid):
    eid = eid
    election_candidates = ElectionCandidate.objects.filter(election_id=eid)
    # total_votes = 0
    candidate_details_list = []
    candidate_votes = {} # dictionary to keep track of candidate votes

    for election_candidate in election_candidates:
        candidate_id = election_candidate.candidate_id
        votes_for_candidate = Vote.objects.filter(eid_id=eid, cid_id=candidate_id).count()
        # total_votes += votes_for_candidate
        candidate_details = Candidate.objects.filter(cid=candidate_id).first()
        candidate_details_list.append(candidate_details)
        candidate_votes[candidate_id] = votes_for_candidate # update the candidate's total votes
        print(candidate_votes[candidate_id])

    context = {'title' : 'Result',
        'election_candidates': election_candidates,
        'candidate_details_list': candidate_details_list,
        'candidate_votes': candidate_votes          # add candidate_votes to the context
    }
    return render(request, 'result.html', context)





def logout_user(request):
    logout(request)
    return render(request, 'home.html')
