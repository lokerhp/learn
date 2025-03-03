# Imports
import argparse
import copy
import glob
import itertools
import os
import pathlib
import re
import shutil
import errno
import git
import json
import ast
import autogenerateSupportedIntegrationsPage as genIntPage


"""
Stages of this ignest sript:

    Stage_1: Ingest every available markdown from the defaultRepos
    
    Stage_2: We create three buckets:
                1. markdownFiles: all the markdown files in defaultRepos
                2. reducedMarkdownFiles: all the markdown files that have hidden metadata fields
                3. toPublish: markdown files that must be included in the learn (metadata_key_value: "learn_status": "Published") 

    Stage_3: 
        1. Move the toPublish markdown files under the DOCS_PREFIX folder based on their metadata (they decide where, 
            they live)
        2. Generate autogenerated pages         
            
    Stage_4: Sanitization
                1. Make the hidden metadata fields actual readable metadata for docusaurus
                2. 
                
    Stage_5: Convert GH links to version specific links
"""



dryRun = False

restFilesDictionary = {}
toPublish = {}
markdownFiles = []
 #Temporarily until we release (change it (the default) to /docs
version_prefix = "nightly"  # We use this as the version prefix in the link strategy
TEMP_FOLDER = "ingest-temp-folder"
defaultRepos = {
    "netdata":
        {
            "owner": "netdata",
            "branch": "master",
        },
    "go.d.plugin":
        {
            "owner": "netdata",
            "branch": "master",
        },
    ".github":
        {
            "owner": "netdata",
            "branch": "main",
        },
    "agent-service-discovery":
        {
            "owner": "netdata",
            "branch": "master",
        }
}


# defaultRepoInaStr = " ".join(defaultRepo)
# print(defaultRepoInaStr)

# Will come back to this once we have a concrete picture of the script
# if sys.argv[1] == "dry-run":
#     print("--- DRY RUN ---\n")
#     dry_run = True

def unSafeCleanUpFolders(folderToDelete):
    """Cleanup every file in the specified folderToDelete."""
    print("Try to clean up the folder: ", folderToDelete)
    try:
        shutil.rmtree(folderToDelete)
        print("Done")
    except Exception as e:
        print("Couldn't delete the folder due to the exception: \n", e)


def safeCleanUpLearnFolders(folderToDelete):
    """
    Cleanup every file in the specified folderToDelete, that doesn't have the `part_of_learn: True`
    metadata in its metadata. It also prints a list of the files that don't have this kind of
    """
    deletedFiles = []
    markdownFiles = fetchMarkdownFromRepo(folderToDelete)
    print("Files in the {} folder #{} which are about to be deleted".format(folderToDelete, len(markdownFiles)))
    unmanagedFiles = []
    for md in markdownFiles:
        metadata = readDocusaurusMetadataFromDoc(md)
        try:
            if "part_of_learn" in metadata.keys():
                # Reductant condition to emphasize what we are looking for when we clean up learn files
                if metadata["part_of_learn"] == "True":
                    pass
            else:
                deletedFiles.append(md)
                os.remove(md)
        except Exception as e:
            print("Couldnt delete the {} file reason: {}".format(md, e))
    print("Cleaned up #{} files under {} folder".format(len(deletedFiles), folderToDelete))
def verifyStringIsDictionary(stringInput):
    try:
        if type(ast.literal_eval(stringInput)) is dict:
            return(True)
        else:
            return(False)
    except:
        return(False)

def unpackDictionaryStringToDictionary(stringInput):
    return(ast.literal_eval(stringInput))

def renameReadmes(fileArray):
    """
    DEPRECATED: to be deleted in v1.0 of this ingest
    In this function we will get the whole list of files,
    search for README named files, and rename them in accordance to their parent dir name.
    After we rename, we need to update the list entry.
    """
    # TODO think of a way of not renaming the unpublished files (?) this will affect only the README s
    counter = 0
    for filename in fileArray:
        if filename.__contains__("README"):
            # Get the path without the filename
            filename = pathlib.Path(filename)
            # And then from that take the last dir, which is the name we want to rename to, add a needed "/" and the
            # ".md"
            newPath = os.path.dirname(filename) + "/" + os.path.basename(filename.parent.__str__()[1:]) + ".md"

            os.rename(filename, newPath)
            fileArray[counter] = newPath
        counter += 1


def copyDoc(src, dest):
    """
    Copy a file
    """
    # Get the path
    try:
        shutil.copy(src, dest)
    except IOError as e:
        # ENOENT(2): file does not exist, raised also on missing dest parent dir
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        os.makedirs(os.path.dirname(dest))
        shutil.copy(src, dest)


def cloneRepo(owner, repo, branch, depth, prefixFolder):
    """
    Clone a repo in a specific depth and place it under the prefixFolder
    INPUTS:
        https://github.com/{owner}/{repo}:{branch}
        as depth we specify the history of the repo (depth=1 fetches only the latest commit in this repo)
    """
    try:
        outputFolder = prefixFolder + repo
        # print("DEBUG", outputFolder)
        git.Git().clone("https://github.com/{}/{}.git".format(owner, repo), outputFolder, depth=depth, branch=branch)
        return "Cloned the {} branch from {} repo (owner: {})".format(branch, repo, owner)
    except Exception as e:
        return (
            "Couldn't clone the {} branch from {} repo (owner: {}) \n Exception {} raised".format(branch, repo, owner,
                                                                                                  e))


def createMDXPathFromMetdata(metadata):
    """
    Create a path from the documents metadata
    REQUIRED KEYS in the metadata input:
        [sidebar_label, learn_rel_path]
    In the returned (final) path we sanitize "/", "//" , "-", "," with one dash
    """
    finalFile = ' '.join(
        (metadata["sidebar_label"].replace("'", " ").replace("/", " ").replace(")", " ").replace(",", " ").replace("(", " ")).split())
    return ("{}/{}/{}.mdx".format(DOCS_PREFIX, \
                                  metadata["learn_rel_path"], \
                                  finalFile.replace(" ", "-")).lower().replace(" ", "-").replace("//", "/"))


def fetchMarkdownFromRepo(outputFolder):
    return glob.glob(outputFolder + '/**/*.md*', recursive=True)


def readHiddenMetadataFromDoc(pathToFile):
    """
    Taking a path of a file as input
    Identify the area with pattern " <!-- ...multiline string -->" and  converts them
    to a dictionary of key:value pairs
    """
    metadataDictionary = {}
    with open(pathToFile, "r+") as fd:
        rawText = "".join(fd.readlines())
        pattern = r"((<!--|---)\n)((.|\n)*?)(\n(-->|---))"
        matchGroup = re.search(pattern, rawText)
        if matchGroup:
            rawMetadata = matchGroup[3]
            listMetadata = rawMetadata.split("\n")
            while listMetadata:
                line = listMetadata.pop(0)
                splitInKeywords = line.split(": ",1)
                key = splitInKeywords[0]
                value = splitInKeywords[1]
                if verifyStringIsDictionary(value):
                    value = unpackDictionaryStringToDictionary(value)
                # If it's a multiline string
                while listMetadata and len(listMetadata[0].split(": ",1)) <= 1:
                    line = listMetadata.pop(0)
                    value = value + line.lstrip(' ')
                value = value.strip("\"")
                metadataDictionary[key] = value.lstrip('>-')
    return metadataDictionary

def readDocusaurusMetadataFromDoc(pathToFile):
    """
    Taking a path of a file as input
    Identify the area with pattern " <!-- ...multiline string -->" and  converts them
    to a dictionary of key:value pairs
    """
    metadataDictionary = {}
    with open(pathToFile, "r+") as fd:
        rawText = "".join(fd.readlines())
        pattern = r"((<!--|---)\n)((.|\n)*?)(\n(-->|---))"
        matchGroup = re.search(pattern, rawText)
        if matchGroup:
            rawMetadata = matchGroup[3]
            listMetadata = rawMetadata.split("\n")
            while listMetadata:
                line = listMetadata.pop(0)
                splitInKeywords = line.split(": ",1)
                key = splitInKeywords[0]
                value = splitInKeywords[1]
                if verifyStringIsDictionary(value):
                    value = unpackDictionaryStringToDictionary(value)
                # If it's a multiline string
                while listMetadata and len(listMetadata[0].split(": ",1)) <= 1:
                    line = listMetadata.pop(0)
                    value = value + line.lstrip(' ')
                value = value.strip("\"")
                metadataDictionary[key] = value.lstrip('>-')
    return metadataDictionary


def sanitizePage(path):
    """
    Converts the
        "<!--" -> "---"
        "-->" -> "---"
    It converts only the first occurrences of these patterns
    Side effect:
        If the document doesn't have purposeful metadata but it contains this pattern in it's body this function replace
        these patterns
    """

    # Open the file for reading
    file = open(path, "r")
    body = file.read()
    file.close()

    # Replace the metadata with comments
    body = body.replace("<!--", "---", 1)
    body = body.replace("-->", "---", 1)

    # The list with the lines that will be written in the file
    output = []

    # For each line of the file I read
    for line in body.splitlines():
        # If the line isn't an H1 title, and it isn't an analytics pixel, append it to the output list
        if not line.startswith("# ") and not line.startswith("[![analytics]"):
            output.append(line + "\n")

    # TODO remove github badges

    # Open the file for overwriting, we are going to write the output list in the file
    file = open(path, "w")
    file.seek(0)
    file.writelines(output)


def convertGithubLinks(path, fileDict, DOCS_PREFIX):
    '''
    Input:
        path: a folder with markdown files
        fileDic: indexes of the ingested documents with their metadata
    Expected format of links in files
        [*](https://github.com/netdata/netdata/blob/master/*)

    '''
    # Open the file for reading
    dummyFile = open(path, "r")
    body = dummyFile.read()
    dummyFile.close()
    output = []

    # For every line in the file we are going to search for urls,
    # and check the dictionary for the relative path of Learn.
    for line in body.splitlines():
        # If in the line there is a link beginning with "]("  then
        if re.search("\]\((.*?)\)", line):
            # Find all the links inside that line
            urls = re.findall("\]\((.*?)\)", line)
            for url in urls:
                # This is replaceString's default value
                replaceString = url
                # If the URL is a GitHub one
                # (at the moment we support this logic only for netdata/netdata links,
                # to keep things simple and test the strategy)
                if url.startswith("https://github.com/netdata/netdata/blob/master"):
                    # temporary link, before we start the slicing and dicing
                    dummy = url.split("https://github.com/netdata/netdata/blob/master")[1]

                    # Try to split the dummy link to the URL and the #link_to_header if any at the end of the URL,
                    # for example split https://github.com/netdata/netdata/blob/rework-learn/docs/glossary.md#c
                    # into "https://github.com/netdata/netdata/blob/master/docs/glossary.md" and "c"
                    try:
                        linkToHeader = dummy.split("#")[1]
                        linkToHeader = "#" + linkToHeader
                    except:
                        linkToHeader = ""

                    # Remove the .md, Docusaurus doesn't work with file extensions in the links
                    dummy = dummy.split(".md")[0]
                    # Break the URL in every "/"
                    dicedURL = dummy.split("/")
                    # THe title of the file
                    urlTitle = dicedURL[len(dicedURL) - 1]
                    # This is the actual link-replacement logic, we check in the file dictionary, if a file is
                    # published, then we know that we can find it (and hence link to it) from within Learn
                    for filename in fileDict:
                        if fileDict[filename]["metadata"]["learn_status"] == "Published":
                            # Again, break the candidate file's learnPath in the "/"s, and remove the file extension
                            dicedCandidateURL = toPublish[filename]['learnPath'].split(".mdx")[0].split("/")

                            # The title of the candidate filepath
                            candidateTitle = dicedCandidateURL[len(dicedCandidateURL) - 1]

                            # Check that the title between the URL and the candidate path is the same, and that it
                            # comes from the same place (this is to take care of duplicate names, for example,
                            # multiple README files)
                            if candidateTitle == urlTitle and \
                                    dicedCandidateURL[len(dicedCandidateURL) - 2] == dicedURL[len(dicedURL) - 2]:
                                # Assign to the replace string the learnPath ("concepts/sampleFolder/sample") without
                                # the file extension
                                replaceString = toPublish[filename]['learnPath'].split(".mdx")[0]
                                # Add "/docs/" IMPORTANT, we need that "/" at the start, Docusaurus handles
                                # "docs/.../..." links differently than "/docs/.../..."
                                # Then add the version prefix
                                # Keep the entire path without the "versioned_docs/version-nightly"
                                # Add the linkToHeader string, if there ain't one it is going to be empty
                                replaceString = "/docs/" + \
                                                version_prefix + \
                                                replaceString.split(DOCS_PREFIX)[1] + \
                                                linkToHeader
                # In the line we are examining, replace the URL string with the new replaceString value
                line = line.replace(url, replaceString)
        # In each iteration we append the new line string, so we essentially re-build the file line-by-line,
        # and in the process some line URLS will be fixed to relative "/docs/" links
        output.append(line + "\n")

    # Write everything onto the file again
    dummyFile = open(path, "w")
    dummyFile.seek(0)
    dummyFile.writelines(output)
    dummyFile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest docs from multiple repositories')

    parser.add_argument(
        '--repos',
        default=[],
        nargs='+',
        help='Choose specific repo you want ingest, if not set, defaults ingested'
    )

    parser.add_argument(
        "-d", "--dry-run",
        help="Don't save a file with the output.",
        action="store_true",
    )

    parser.add_argument(
        "--docs-prefix",
        help="Don't save a file with the output.",
        dest="DOCS_PREFIX",
        default="versioned_docs/version-nightly"
    )


    listOfReposInStr = []
    # netdata/netdata:branch tkatsoulas/go.d.plugin:mybranch
    args = parser.parse_args()
    kArgs = args._get_kwargs()
    '''Create local copies from the argpase input'''
    DOCS_PREFIX = args.DOCS_PREFIX
    for x in kArgs:
        if x[0] == "repos":
            listOfReposInStr = x[1]
        if x[0] == "dryRun":
            print(x[1])
            dryRun = x[1]

    if len(listOfReposInStr) > 0:
        for repoStr in listOfReposInStr:
            try:
                _temp = repoStr.split("/")
                owner, repo, branch = [_temp[0]] + (_temp[1].split(":"))
                defaultRepos[repo]["owner"] = owner
                defaultRepos[repo]["branch"] = branch
            except(TypeError, ValueError):
                print("You specified a wrong format in at least one of the repos you want to ingest")
                parser.print_usage()
                exit(-1)
            except KeyError:
                print(repo)
                print("The repo you specified in not in predefined repos")
                print(defaultRepos.keys())
                parser.print_usage()
                exit(-1)
            except Exception as e:
                print("Unknown error in parsing", e)

    '''
    Clean up old clones into a temp dir
    '''
    unSafeCleanUpFolders(TEMP_FOLDER)
    '''
    Clean up old ingested docs
    '''
    safeCleanUpLearnFolders(DOCS_PREFIX)
    print("Creating a temp directory: ",TEMP_FOLDER)
    try:
        os.mkdir(TEMP_FOLDER)
    except FileExistsError:
        print("Folder already exists")

    '''
    Clean up old docs
    '''
    #unSafeCleanUpFolders(DOCS_PREFIX)

    '''Clone all the predefined repos'''
    for key in defaultRepos.keys():
        print(cloneRepo(defaultRepos[key]["owner"], key, defaultRepos[key]["branch"], 1, TEMP_FOLDER + "/"))
    # This line is useful only during the rework
    #print(cloneRepo("netdata", "learn", "rework-learn", 1, TEMP_FOLDER + "/"))
    # We fetch the markdown files from the repositories
    markdownFiles = fetchMarkdownFromRepo(TEMP_FOLDER)

    print("Files detected: ", len(markdownFiles))
    print("Gathering Learn files...")
    # After this we need to keep only the files that have metadata, so we will fetch metadata for everything and keep
    # the entries that have populated dictionaries
    reducedMarkdownFiles = []
    for md in markdownFiles:
        #print("File: ", md)
        metadata = readHiddenMetadataFromDoc(md)
        # Check to see if the dictionary returned is empty
        if len(metadata) > 0:
            #print(metadata)
            reducedMarkdownFiles.append(md)
            if "learn_status" in metadata.keys():
                if metadata["learn_status"] == "Published":
                    try:
                        toPublish[md] = {
                            "metadata": metadata,
                            "learnPath": str(createMDXPathFromMetdata(metadata)),
                            "ingestedRepo": str(md.split("/", 2)[1])
                        }
                    except:
                        print("File {} doesnt container key-value {}".format(md, KeyError))
            else:
                restFilesDictionary[md] = {
                    "metadata": metadata,
                    "learnPath": str("docs/_archive/_{}".format(md)),
                    "ingestedRepo": str(md.split("/", 2)[1])
                }

        del metadata
    # we update the list only with the files that are destined for Learn

    # FILE MOVING
    print("Moving files...")

    # identify published documents:q
    print("Found Learn files: ", len(toPublish))
    #print(json.dumps(toPublish, indent=4))
    for file in toPublish:
        copyDoc(file, toPublish[file]["learnPath"])
        sanitizePage(toPublish[file]["learnPath"])
    for file in restFilesDictionary:
        pass
        # moveDoc(file, restFilesDictionary[file]["learnPath"])
    print("Generating integrations page")
    genIntPage.generate(toPublish, DOCS_PREFIX+"/getting-started/integrations.mdx")
    print("Done")
    print("Fixing github links...")
    # After the moving, we have a new metadata, called newLearnPath, and we utilize that to fix links that were
    # pointing to GitHub relative paths
    for file in toPublish:
        convertGithubLinks(toPublish[file]["learnPath"], toPublish, DOCS_PREFIX)
    print("These files are in repos and dont have valid metadata to publish them in learn")
    for file in restFilesDictionary:
        if "custom_edit_url" in restFilesDictionary[file]["metadata"]:
            print(restFilesDictionary[file]["metadata"]["custom_edit_url"])
        else:
            print("Custom edit url not found, printing any metadata and its position when we ingest it" )
            print(json.dumps(restFilesDictionary[file]["metadata"], indent=4))
            print("&Position: ", file)
    print("Done.")

    unSafeCleanUpFolders(TEMP_FOLDER)

print("OPERATION FINISHED")
