---
title: "Test and validate the CMS open data environment"
teaching: 10
exercises: 30
questions:
- "What is in the CMSSW Docker image?"
- "How do I test and validate my CMSSW Docker container?"
objectives:
- "Learn about the details of the CMS Docker container"
- "Test and validate the CMS Docker image by running a CMSSW job."
keypoints:
- "The CMS Docker image contains all the required ingredients to start analyzing CMS open data."
- "In order to test and validate the Docker container you can run a simple CMSSW job."  
---
<!--
> ## Helpline
>
> Remember that we are always available to help.  Our [Mattermost](https://mattermost.web.cern.ch/cmsodws2021/channels/docker-pre-exercise) channel is open.
{: .callout}
-->

## The CMS open data containers

In the previous page, you have downloaded the three different containers that will be used in this tutorial: the CMSSW container, the root container and the python container. You've tested that you can open the graphical user interface. The CMSSW container is mandatory to access to the CMS open data files. Therefore, in this section, you'll make sure that you can run a CMSSW job and access to the data files. 


## Know your Docker image

The Docker container we just created provides CMS computing environment to be used with the 2015 CMS open data. The Docker container uses Scientific Linux CERN.  As it was mentioned before, it comes equipped with the [ROOT](http://root.cern.ch/) framework and the version of [CMS Software - CMSSW](http://cms-sw.github.io/) compatible with the CMS open data.

Access to the data is through the [XRootD](https://xrootd.slac.stanford.edu/) protocol.

## The working directory

When your Docker container starts up with the volume mount option `-v ${HOME}/cms_open_data_work:/home/cmsusr`, everything that is in the container's `/home/cmsusr` directory is also visible in your local computer's `${HOME}/cms_open_data_work`. You will therefore see `CMSSW_7_6_7/src` on your local computer, and you will be able to edit files there. The changes will take effect also on the files in the container.

Remember that whatever you have in the local directory `cms_open_data_work` will be visible in the container. If you need to create a new container, make sure that you pass a fresh directory, or that you are sure that the old files are those that you want to pass to your new container.

> ## Warning!
> If you did not create the directory on your local computer before creating the container, it is created automatically but with the wrong user/group. When starting the container, you will get a message `cannot make directory CMSSW_7_6_7 Permission denied`
{: .callout}


## Run a simple *demo* for testing and validating

The validation procedure tests that the CMS environment is installed and operational on your Docker container, and that you have access to the CMS Open Data files. These steps also give you a quick introduction to the CMS environment.

Verify first that you are in ```~/CMSSW_7_6_7/src``` directory in your container. You can check that with command `pwd`.

<!--
> ## Work assignment
>
> This is a good moment to go to our [assignment form](https://forms.gle/DDboG1MCcSNRBRHFA) and answer some simple questions for this pre-exercise; you must sign in and <strong style="color: red;">click on the submit button</strong> in order to save your work.  You can go back to edit the form at any time.
{: .challenge} -->

Create a working directory for the demo analyzer, change to that directory and create a *skeleton* for the analyzer:

~~~
mkdir Demo
cd Demo
mkedanlzr DemoAnalyzer
~~~
{: .language-bash}

Compile the code:

~~~
scram b
~~~
{: .language-bash}

and you will get output similar to this:

~~~
$ scram b
>> Local Products Rules ..... started
>> Local Products Rules ..... done
>> Entering Package Demo/DemoAnalyzer
>> Creating project symlinks
  src/Demo/DemoAnalyzer/python -> python/Demo/DemoAnalyzer
Entering library rule at src/Demo/DemoAnalyzer/plugins
>> Compiling edm plugin /home/cmsusr/CMSSW_7_6_7/src/Demo/DemoAnalyzer/plugins/DemoAnalyzer.cc
>> Building edm plugin tmp/slc6_amd64_gcc493/src/Demo/DemoAnalyzer/plugins/DemoDemoAnalyzerAuto/libDemoDemoAnalyzerAuto.so
Leaving library rule at src/Demo/DemoAnalyzer/plugins
@@@@ Running edmWriteConfigs for DemoDemoAnalyzerAuto
--- Registered EDM Plugin: DemoDemoAnalyzerAuto
>> Leaving Package Demo/DemoAnalyzer
>> Package Demo/DemoAnalyzer built
>> Subsystem Demo built
>> Local Products Rules ..... started
>> Local Products Rules ..... done
gmake[1]: Entering directory `/code/CMSSW_7_6_7'
>> Creating project symlinks
  src/Demo/DemoAnalyzer/python -> python/Demo/DemoAnalyzer
>> Done python_symlink
>> Compiling python modules python
>> Compiling python modules src/Demo/DemoAnalyzer/python
>> All python modules compiled
@@@@ Refreshing Plugins:edmPluginRefresh
>> Pluging of all type refreshed.
>> Done generating edm plugin poisoned information
gmake[1]: Leaving directory `/code/CMSSW_7_6_7'
~~~
{: .output}

Before launching the job, let's modify the configuration file (do not worry, you will learn about all this stuff in a different [lesson](https://cms-opendata-workshop.github.io/workshop2022-lesson-cmssw/)) so that it will read a CMS open data file.

Open the `ConfFile_cfg.py` in the `Demo/DemoAnalyzer/python` directory with your normal editor on your local computer.You will find the `Demo` area under the  `cms_open_data_work/CMSSW_7_6_7/src` directory on your local computer. As the working directory has been mounted into the container, all changes take effect there as well. 

Replace `file:myfile.root` with `root://eospublic.cern.ch//eos/opendata/cms/Run2015D/SingleElectron/MINIAOD/08Jun2016-v1/10000/001A703B-B52E-E611-BA13-0025905A60B6.root` to point to an example file.

Chage also the maximum number of events to 10.  I.e., change `-1`to `10` in `process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))`.

> ## Take a look at the final validation config file
>
> At the end, the config file should look like
>
> ~~~
> import FWCore.ParameterSet.Config as cms
> process = cms.Process("Demo")
> process.load("FWCore.MessageService.MessageLogger_cfi")
> process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
> process.source = cms.Source("PoolSource",
> # replace 'myfile.root' with the source file you want to use
>    fileNames = cms.untracked.vstring(
>        'root://eospublic.cern.ch//eos/opendata/cms/Run2015D/SingleElectron/MINIAOD/08Jun2016-v1/10000/001A703B-B52E-E611-BA13-0025905A60B6.root'
>    )
> )
>
> process.demo = cms.EDAnalyzer('DemoAnalyzer'
> )
>
> process.p = cms.Path(process.demo)
> ~~~
> {: .language-python}
{: .solution}


Finally, run the cms executable with our configuration:
~~~
cmsRun DemoAnalyzer/python/ConfFile_cfg.py
~~~
{: .language-bash}

~~~
10-Jul-2022 18:44:42 CEST  Initiating request to open file root://eospublic.cern.ch//eos/opendata/cms/Run2015D/SingleElectron/MINIAOD/08Jun2016-v1/10000/001A703B-B52E-E611-BA13-0025905A60B6.root
220710 18:44:42 570 secgsi_InitProxy: cannot access private key file: /home/cmsusr/.globus/userkey.pem
%MSG-w XrdAdaptor:  file_open 10-Jul-2022 18:44:43 CEST pre-events
Data is served from cern.ch instead of original site eospublic
%MSG
10-Jul-2022 18:44:44 CEST  Successfully opened file root://eospublic.cern.ch//eos/opendata/cms/Run2015D/SingleElectron/MINIAOD/08Jun2016-v1/10000/001A703B-B52E-E611-BA13-0025905A60B6.root
Begin processing the 1st record. Run 257645, Event 1184198851, LumiSection 776 at 10-Jul-2022 18:44:59.914 CEST
Begin processing the 2nd record. Run 257645, Event 1184202760, LumiSection 776 at 10-Jul-2022 18:44:59.916 CEST
Begin processing the 3rd record. Run 257645, Event 1183968519, LumiSection 776 at 10-Jul-2022 18:44:59.917 CEST
Begin processing the 4th record. Run 257645, Event 1183964627, LumiSection 776 at 10-Jul-2022 18:44:59.917 CEST
Begin processing the 5th record. Run 257645, Event 1184761030, LumiSection 776 at 10-Jul-2022 18:44:59.918 CEST
Begin processing the 6th record. Run 257645, Event 1184269130, LumiSection 776 at 10-Jul-2022 18:44:59.918 CEST
Begin processing the 7th record. Run 257645, Event 1184358918, LumiSection 776 at 10-Jul-2022 18:44:59.918 CEST
Begin processing the 8th record. Run 257645, Event 1183874827, LumiSection 776 at 10-Jul-2022 18:44:59.919 CEST
Begin processing the 9th record. Run 257645, Event 1184415529, LumiSection 776 at 10-Jul-2022 18:44:59.919 CEST
Begin processing the 10th record. Run 257645, Event 1184425291, LumiSection 776 at 10-Jul-2022 18:44:59.919 CEST
10-Jul-2022 18:44:59 CEST  Closed file root://eospublic.cern.ch//eos/opendata/cms/Run2015D/SingleElectron/MINIAOD/08Jun2016-v1/10000/001A703B-B52E-E611-BA13-0025905A60B6.root

=============================================

MessageLogger Summary

 type     category        sev    module        subroutine        count    total
 ---- -------------------- -- ---------------- ----------------  -----    -----
    1 XrdAdaptor           -w file_open                              1        1
    2 fileAction           -s file_close                             1        1
    3 fileAction           -s file_open                              2        2

 type    category    Examples: run/evt        run/evt          run/evt
 ---- -------------------- ---------------- ---------------- ----------------
    1 XrdAdaptor           pre-events
    2 fileAction           PostEndRun
    3 fileAction           pre-events       pre-events

Severity    # Occurrences   Total Occurrences
--------    -------------   -----------------
Warning                 1                   1
System                  3
~~~
{: .output}

Congratulations! You are all set with your Docker environment.

> ## Work assignment
>
> Now, submit your assignment for this lesson.  You will find a task in our [assignment form](https://forms.gle/7YYRv6ZCTfRYiocr7); remember you must sign in and <strong style="color: red;">click on the submit button</strong> in order to save your work.  You can go back to edit the form at any time.
{: .challenge}

<blockquote class="testimonial">
  <p> Problems have been reported running amd-based containers such as this on MacOS with M1 chip. Increasing the memory available to Docker may help. Please check the possible solutions in <a href="https://opendata-forum.cern.ch/t/cms-open-data-docker-test-and-validate-error/111/12">this post</a> in the CERN Open Data forum. Note, however, that this may help you to open the container, but it is very likely that problems remain when you try to compile code and run jobs in it.</p> <p>For the CMS open data workshop, we provide a <a href=" http://docker.cms-cloud.net/">temporary solution</a> which gives a docker environment in browser. You can use it for the CMSSW container during the lessons, if needed. Note the following: <ul>
  <li>in the "Play with docker" terminal, after having created the working directory and before starting the container, change the permission of the working directory with <code class="language-plaintext highlighter-rouge">chmod 777 cms_open_data_work</code></li>
  <li>if you use the editor that comes with "Play with docker", the owner of the edited file needs to be changed back in the container with <code class="language-plaintext highlighter-rouge">sudo chown $USER file-name</code></li>
  <li>for the vnc in browser, open it by cliking "Open port", give 6080 and then add <code class="language-plaintext highlighter-rouge">vnc.html</code> in the URL of the tab that opens.</li></ul>The other containers used in this workshop should run fine on MacOS with M1 chip.</p></blockquote>

> ## CMSSW jobs still not running in a container on a MacOS with M1 chip?
> If increasing memory for Docker did not help, there's not much we can do. But this is not a show-stopper, you can still work with the CMS Open data, but you have to work differently. You will not be able to run CMSSW jobs in the CMSSW open data container on your own laptop, but you can still use the container. We propose the following:
> 
> - run the quick examples and tests as GitHub actions using the CMSSW container (in which case your jobs run on GitHub "runners") and download the ouput files as "artifacts" (an example is coming soon)
> - for any larger production, you would in any case use other resources than your own laptop, you will learn more about that in the cloud tutorial
> - you can still use the two other containers (for ROOT and python) to inspect the output of your jobs.
>
> To run a short CMSSW example job as a GitHub workflow, first go to the [example repository](https://github.com/cms-opendata-workshop/workshop2022-CMSSW-container-demo). The repository contains the example code generated above, with the two modifications in the configuration file for the file name and the number of events. To get your own version of it click on the arrow to the right of Fork (top right), and choose "Create a new fork". 
>
> In your new repository, go to the Actions tab, and click on "I understand my workflow, go ahead and enable them". Choose the workflow "Test CMSSW on plain docker" and run the workflow by selecting branch `docker-04` under "Run workflow".
>
> ![](../assets/img/github_action_run_workflow.png)
> You can follow the job progress and output by clicking on "DemoAnalyzer test - plain docker" and expanding on "Going to a container", and if the job finishes with success, you will find the ouput under "Artifacts" in the workflow summary. In this example, it is the ouput log from the job above, but you could eventually produce some data files later on during this workshop and download them from the same place.
>
> Note that every time the workflow runs it takes several minutes to start, as it needs to download the container image. This certainly not ideal for quick testing, but remember that this is a workaround as you were not able to run jobs on the container locally.
>
> The workflow is defined in `.github/workflows/main.yaml` and the commands that are passed into the container are in `commands.sh` in branch `docker-04` of the repository.
{: .solution}

{% include links.md %}
