# =====================================================
# AI FURNITURE OS V3
# SYSTEM CORE INSTALLER
# =====================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=========================================="
Write-Host " INSTALLING AIFOS SYSTEM CORE "
Write-Host "=========================================="



# -----------------------------
# system_controller.py
# -----------------------------

@'
from .module_scanner import ModuleScanner
from .health_monitor import HealthMonitor
from .system_reporter import SystemReporter


class SystemController:

    def __init__(self):

        self.scanner = ModuleScanner()
        self.health = HealthMonitor()
        self.reporter = SystemReporter()


    def run(self):

        modules = self.scanner.scan()

        health = self.health.check(
            modules
        )

        report = self.reporter.create(
            modules,
            health
        )

        return report
'@ | Set-Content brain\system\system_controller.py



# -----------------------------
# module_scanner.py
# -----------------------------

@'
import os


class ModuleScanner:


    def scan(self):

        root = "brain"

        modules = []

        ignore = [
            "legacy",
            "__pycache__"
        ]


        for item in os.listdir(root):

            path = os.path.join(
                root,
                item
            )

            if os.path.isdir(path):

                if item not in ignore:

                    modules.append(
                        item
                    )


        return {
            "modules": modules,
            "count": len(modules)
        }
'@ | Set-Content brain\system\module_scanner.py



# -----------------------------
# health_monitor.py
# -----------------------------

@'
class HealthMonitor:


    def check(self, modules):

        score = 100


        if modules["count"] == 0:

            score = 0


        return {

            "score": score,

            "status":
                "healthy"
                if score >= 80
                else
                "warning"

        }
'@ | Set-Content brain\system\health_monitor.py



# -----------------------------
# change_detector.py
# -----------------------------

@'
import subprocess


class ChangeDetector:


    def detect(self):

        result = subprocess.run(
            [
                "git",
                "status",
                "--porcelain"
            ],
            capture_output=True,
            text=True
        )


        return {

            "changed":
                bool(result.stdout.strip()),

            "files":
                result.stdout.splitlines()

        }
'@ | Set-Content brain\system\change_detector.py



# -----------------------------
# backup_manager.py
# -----------------------------

@'
import os
import shutil
from datetime import datetime


class BackupManager:


    def create(self):

        folder = (
            "brain/system/backups/"
            +
            datetime.now()
            .strftime("%Y%m%d_%H%M%S")
        )

        os.makedirs(
            folder,
            exist_ok=True
        )


        return folder
'@ | Set-Content brain\system\backup_manager.py



# -----------------------------
# version_manager.py
# -----------------------------

@'
class VersionManager:


    def current(self):

        return {

            "system":
                "AIFOS V3",

            "layer":
                "Autonomous Manager"

        }
'@ | Set-Content brain\system\version_manager.py



# -----------------------------
# system_memory.py
# -----------------------------

@'
import json
import os


class SystemMemory:


    file = (
        "brain/system/system_state.json"
    )


    def save(self,data):

        with open(
            self.file,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )


    def load(self):

        if not os.path.exists(
            self.file
        ):

            return {}

        with open(
            self.file,
            encoding="utf8"
        ) as f:

            return json.load(f)
'@ | Set-Content brain\system\system_memory.py



# -----------------------------
# system_reporter.py
# -----------------------------

@'
import json


class SystemReporter:


    def create(
        self,
        modules,
        health
    ):


        report = {

            "modules":
                modules,

            "health":
                health

        }


        with open(
            "docs/system_report.json",
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )


        return report
'@ | Set-Content brain\system\system_reporter.py



Write-Host ""
Write-Host "=========================================="
Write-Host " SYSTEM CORE INSTALLED "
Write-Host "=========================================="