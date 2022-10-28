import os
import subprocess
import argparse


def get_commit_message():
    """Retrieve the commit message."""
    build_source_version_message = os.environ["BUILD_SOURCEVERSIONMESSAGE"]

    if os.environ["BUILD_REASON"] != "PullRequest":
        return build_source_version_message

    # By default pull requests use refs/pull/PULL_ID/merge as the source branch
    # which has a "Merge ID into ID" as a commit message. The latest commit
    # message is the second to last commit
    commit_id = build_source_version_message.split()[1]
    git_cmd = ["git", "log", commit_id, "-1", "--pretty=%B"]
    return subprocess.run(
        git_cmd, capture_output=True, text=True
    ).stdout.strip()


def parsed_args():
    parser = argparse.ArgumentParser(
        description=(
            "Show commit message that triggered the build in Azure DevOps pipeline"
        )
    )
    parser.add_argument(
        "--only-show-message",
        action="store_true",
        default=False,
        help=(
            "Only print commit message. Useful for direct use in scripts rather than"
            " setting output variable of the Azure job"
        ),
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parsed_args()
    commit_message = get_commit_message()

    if args.only_show_message:
        print(commit_message)
    else:
        # set the environment variable to be propagated to other steps
        print(f"##vso[task.setvariable variable=message;isOutput=true]{commit_message}")
        print(f"commit message: {commit_message}")  # helps debugging
