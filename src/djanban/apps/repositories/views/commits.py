# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import shutil
import zipfile

import shortuuid
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from djanban.apps.base.decorators import member_required
from djanban.apps.repositories.forms import CommitForm, DeleteCommitForm, MakeAssessmentForm
from djanban.apps.repositories.models import Commit, PylintMessage, PhpMdMessage
from djanban.apps.repositories.phpmd import PhpDirectoryAnalyzer
from djanban.apps.repositories.pylinter import PythonDirectoryAnalyzer


@member_required
def add(request, board_id, repository_id):
    member = request.user.member
    try:
        board = member.boards.get(id=board_id)
        repository = board.repositories.get(id=repository_id)
    except ObjectDoesNotExist:
        raise Http404

    commit = Commit(board=board, repository=repository)

    if request.method == "POST":
        form = CommitForm(request.POST, request.FILES, instance=commit)

        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse("boards:repositories:view_repository", args=(board_id, repository_id)))

    else:
        form = CommitForm(instance=commit)

    replacements = {"form": form, "board": board, "member": member, "repository": repository}
    return render(request, "repositories/commits/add.html", replacements)


# Delete a commit
@member_required
def delete(request, board_id, repository_id, commit_id):
    member = request.user.member
    try:
        board = member.boards.get(id=board_id)
        repository = board.repositories.get(id=repository_id)
        commit = repository.commits.get(id=commit_id)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == "POST":
        form = DeleteCommitForm(request.POST)

        if form.is_valid() and form.cleaned_data.get("confirmed"):
            commit.delete()
            return HttpResponseRedirect(reverse("boards:repositories:view_repository", args=(board_id, repository_id)))

    else:
        form = DeleteCommitForm()

    replacements = {"form": form, "board": board, "member": member, "repository": repository, "commit": commit}
    return render(request, "repositories/commits/delete.html", replacements)


# View assessment report
@member_required
def view_assessment_report(request, board_id, repository_id, commit_id):
    member = request.user.member
    try:
        board = member.boards.get(id=board_id)
        repository = board.repositories.get(id=repository_id)
        commit = repository.commits.get(id=commit_id)
    except ObjectDoesNotExist:
        raise Http404

    language = request.GET.get("language")

    pylint_filter = request.GET.get("type")
    pyint_messages = commit.pylint_messages.all()
    if pylint_filter and language == "python":
        pyint_messages = pyint_messages.filter(type=pylint_filter)

    phpmd_filter = request.GET.get("ruleset")
    phpmd_messages = commit.phpmd_messages.all()
    if phpmd_filter and language == "php":
        phpmd_messages = phpmd_messages.filter(ruleset=phpmd_filter)

    replacements = {
        "board": board, "member": member, "repository": repository, "commit": commit,
        "commit_files": commit.files.all(),
        "pylint_messages": pyint_messages,
        "pylint_filter_values": PylintMessage.TYPE_CHOICES,
        "pylint_filter": pylint_filter,
        "phpmd_filter_values": PhpMdMessage.RULESETS,
        "phpmd_messages": phpmd_messages,
        "phpmd_filter": phpmd_filter
    }
    return render(request, "repositories/commits/assessment/view_report.html", replacements)

