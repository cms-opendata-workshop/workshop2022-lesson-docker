---
title: "Using Docker with the CMS open data"
teaching: Self-guided
exercises: 40 
questions:
- "How do I use docker to effectively interface with the CMS open data?"
- "What container images are available for my work with the CMS open data?"
objectives:
- "Download the CMSSW open data docker image"
- "Open your own CMSSW open data container and check that graphical windows open"
- "Download the ROOT and python images and build your own container"
- "Restart an existing container"
- "Delete and rebuild containers"
keypoints:
- "You have now set up a docker container as a working enviroment for CMS open data. You know how to open a graphical window in it and how to pass files between your own computer and the container."

---

## Overview

This exercise will walk you through setting up and familiarizing yourself with Docker, so that
you can effectively use it to interface with the CMS open data. It is *not* meant to completely
cover containers and everything you can do with Docker. <!--- Reach out to the organizers
using the [dedicated Mattermost channel][mattermost]
if we are missing something. -->

Three types of container images are provided: [one with the CMS software (CMSSW)](https://gitlab.cern.ch/cms-cloud/cmssw-docker-opendata/-/blob/master/README.md) compatible with the released data, and two others with [ROOT](https://gitlab.cern.ch/cms-cloud/root-vnc) and [python](https://gitlab.cern.ch/cms-cloud/python-vnc) libraries needed in this workshop. The CMSSW container is mandatory if you want to access the CMS data in AOD and MiniAOD formats (you will learn about them later), as you will not be able to install CMSSW software on your own computer. The two others are provided to make setting up and using ROOT and/or python libraries easier for you for this tutorial, but if you wish, you can also install them on your computer. 

All container images come with [VNC](https://gitlab.cern.ch/cms-cloud/cmssw-docker-opendata/-/blob/master/README.md#use-vnc) for the graphical use interface. It opens directly in a browser window. Optionally, you can also connect to the VNC server of the container using a VNC viewer (VNC viewer (TigerVNC, RealVNC, TightVNC, OSX built-in VNC viewer, etc.) installed on your local machine, but only the browser option for which no additional tools are needed is described in these instructions. On native Linux, you can also use X11-forwarding.

For different CMSSW container images, some guidance can be found on the
[Open Data Portal introduction to Docker](http://opendata.cern.ch/docs/cms-guide-docker). In this tutorial, we will use the container image needed for the CMS open data from 2015. The use of graphical interfaces, such the graphics window from ROOT, depends on the operating system of your computer. Therefore, in the following, separate instructions are given for Windows WSL, Linux and MacOS.

> Note that the container images are large (the compressed download size is 6.6GB for the CMSSW container, and of order of 1GB for the ROOT and python containers). Make sure that you make it in time to download them and work through the exercises before the workshop.
{: .testimonial}


## Download the docker image for CMSSW open data and start a container

The first time you start a container, a docker image file gets downloaded from an image registry. The CMSSW open data image is large (6.6GB) and it may take very long to
download, depending on the speed of your internet
connection. After the download, a container created from that image starts. The image download needs to be done only once. Afterwards, when starting a container, it will find the downloaded image on your computer, and it will be much faster.

The containers do not have modern editors and it is expected that you mount your working directory from the local computer into the container, and use your normal editor for editing the files. Note that all your compiling and executing still has to be done *in the Docker container*!

First, before you start up your container, create a local directory
where you will be doing your code development. In the example below, it is called
`cms_open_data_work` and it will live in the `$HOME` directory. You may choose a different location and a shorter directory name if you like. :)

> ## Local machine
> ~~~
> cd # This is to make sure I'm in my home directory
> mkdir cms_open_data_work
> ~~~
> {: .language-bash}
{: .challenge}

> ## Warning!
> If you do not create the directory on your local computer before creating the container, the directory is created automatically but with the wrong user/group. When starting the container, you will get a message `cannot make directory CMSSW_7_6_7 Permission denied`. In that case, delete the directory with `rm -rf cms_open_data_work/`, and remove the failing container with `docker rm <container-name>` so that you can use the same name. In the following, we will use `my_od` as the container name. And then, remember to create the directory before creating the container!
{: .callout}

Start the container following the instructions below depending on the operating system you are using.

<div id="docker-run">

    <div>
        <ul class="nav nav-tabs" role="tablist">
        <li role="presentation" class="active"><a data-os="linux" href="#shell-linux" aria-controls="Linux" role="tab" data-toggle="tab">Linux</a></li>
        <li role="presentation"><a data-os="windows" href="#shell-windows" aria-controls="Windows" role="tab" data-toggle="tab">Windows WSL2</a></li>
        <li role="presentation"><a data-os="macos" href="#shell-macos" aria-controls="MacOS" role="tab" data-toggle="tab">MacOS</a></li>
        </ul>

        <div class="tab-content">

            <article role="tabpanel" class="tab-pane active" id="shell-linux">

<p>We will use the <code class="language-plaintext highlighter-rouge">docker run</code> command to create the container (downloading the appropriate image if it is the first time) and start it right away.</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>docker run -it --name my_od --net=host --env="DISPLAY" -v $HOME/.Xauthority:/home/cmsusr/.Xauthority:rw  -v ${HOME}/cms_open_data_work:/code cmsopendata/cmssw_7_6_7-slc6_amd64_gcc493 /bin/bash
</code></pre></div></div>
                       
<div class="language-plaintext output highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Setting up CMSSW_7_6_7
CMSSW should now be available.
This is a standalone image for CMSSW_7_6_7 slc6_amd64_gcc493.
(/code/CMSSW_7_6_7/src)
</code></pre></div></div>

<p>This is now a bash shell in the CMS open data environment in which you have access to a complete CMS software release that is appropriate for interfacing with the 2015 13 TeV datasets.</p>
              
<p>As there are rate limits for pulls from Docker Hub, you may get the following error message: <code class="language-plaintext highlighter-rouge">docker: Error response from daemon: toomanyrequests: You have reached your pull rate limit. You may increase the limit by authenticating and upgrading.</code>. In that case, try later (the limit is per 6 hours) or use the mirror <code class="language-plaintext highlighter-rouge">gitlab-registry.cern.ch/cms-cloud/cmssw-docker-opendata/cmssw_7_6_7-slc6_amd64_gcc493</code> instead of <code class="language-plaintext highlighter-rouge">cmsopendata/cmssw_7_6_7-slc6_amd64_gcc493</code>.</p>

<p>Now let’s understand the options that were used for the <code class="language-plaintext highlighter-rouge">docker run</code> command.</p>

<ul>
  <li>First, the <code class="language-plaintext highlighter-rouge">-it</code> (or <code class="language-plaintext highlighter-rouge">-i</code>) option means to start the container in interactive mode. Essentially, it means that you will end up inside the running container.</li>
  <li>We assign a name to the container using the <code class="language-plaintext highlighter-rouge">--name</code> switch, so that we can refer back to this environment and still access any files we created in there. You can, of course, choose a different name than <code class="language-plaintext highlighter-rouge">my_od</code>.</li>
  <li>The <code class="language-plaintext highlighter-rouge">--net=host</code> switch will allow you to use the host network (Internet access) in the container.</li>
  <li>The <code class="language-plaintext highlighter-rouge">--env</code> switch will forward the appropiate <code class="language-plaintext highlighter-rouge">DISPLAY</code> environmental variable from the host machine to the container so X11-forwarding (the ability to open graphical windows inside the container) can be achieved.</li>
  <li>For X11-forwarding to be functional, your local <code class="language-plaintext highlighter-rouge">$HOME/.Xauthority</code> file needs to be mounted as the <code class="language-plaintext highlighter-rouge">/home/cmsusr/.Xauthority</code> file inside the container.  We do this using the <code class="language-plaintext highlighter-rouge">--volume</code> (or <code class="language-plaintext highlighter-rouge">-v</code>) switch. Note that the colon (<code class="language-plaintext highlighter-rouge">:</code>) symbol separates the source and destination points for the mounting procedure. In addition, the <code class="language-plaintext highlighter-rouge">rw</code> tag is given (aslo separated by <code class="language-plaintext highlighter-rouge">:</code>) so it can be read and written if necessary. </li>
  <li>With <code class="language-plaintext highlighter-rouge">-v ${HOME}/cms_open_data_work:/code</code>, the working directory <code class="language-plaintext highlighter-rouge">cms_open_data_work</code> that you created in your home directory is mounted with the <code class="language-plaintext highlighter-rouge">-v</code> option into the container's <code class="language-plaintext highlighter-rouge">/code</code> directory. This makes it possible to edit files in the CMSSW area of your container with your normal editor on your local computer.</li>
  <li><code class="language-plaintext highlighter-rouge">cmsopendata/cmssw_7_6_7-slc6_amd64_gcc493</code> is the name of the image we will use. If no label is prepended, Docker assumes that it resides in <a href="https://hub.docker.com/">Docker Hub</a>, the official image repository of Docker.</li>
  <li>Finally, the <code class="language-plaintext highlighter-rouge">/bin/bash</code> option will throw the container into a <code class="language-plaintext highlighter-rouge">bash</code> shell when running interactively.</li>
</ul>

<p>For a more complete listing of options, see <a href="https://docs.docker.com/engine/reference/commandline/container_run/">the official Docker documentation</a> on the <code class="language-plaintext highlighter-rouge">docker run</code> command.</p>

<p>To test that X11-forwarding works, start the ROOT program by typing <code class="language-plaintext highlighter-rouge">root</code> in the container prompt. In ROOT prompts , type <code class="language-plaintext highlighter-rouge">TBrowser t</code> to open the ROOT graphical window. If the graphical window opens you are all set and you can exit from ROOT either by choosing the option from the TBrowser window or by typing <code class="language-plaintext highlighter-rouge">.q</code> in the ROOT prompt.</p>

<p>Make sure that you can copy instructions from a browser page to the container terminal. One thing you can try is <code class="language-plaintext highlighter-rouge">Shift+Ctrl+V</code> when pasting into your container terminal, rather than <code class="language-plaintext highlighter-rouge">Ctrl-V</code>. That sometimes will work. If not, you will see later in these instructions how to pass files from your local computer to the container.</p>

<p>Then type <code class="language-plaintext highlighter-rouge">exit</code> to leave the container.</p>

<p>If you find that X11 forwarding is not working and the ROOT graphical window does not open, try typing the following before starting your Docker container.</p>
<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>xhost <span class="nb">local</span>:root
</code></pre></div></div>

<p>If everything works fine, you are ready to continue with the lesson.</p>

<blockquote class="solution">
  <h2 id="if-you-still-have-problems-with-x11-forwarding">If you still have problems with X11 forwarding</h2>

  <p><strong>In the case you are having problems with X11 forwarding</strong>, there is the option of using a VNC application installed in the container image:</p>

  <div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>docker run -it --name my_od -P -p 5901:5901  -p 6080:6080 -v ${HOME}/cms_open_data_work:/code cmsopendata/cmssw_7_6_7-slc6_amd64_gcc493:latest /bin/bash
</code></pre></div>  </div>
  
  <p>This container has a VNC application installed to allow opening graphical windows on a remote machine (seen from the container, your own computer is a remote machine). Start the application with <code class="language-plaintext highlighter-rouge">start_vnc</code> from your container prompt. You will need to start it every time you use the container (if you want to open graphics windows).</p>

  <div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>start_vnc
</code></pre></div></div>

  <div class="language-plaintext output highlighter-rouge"><div class="highlight"><pre class="highlight"><code>xauth:  file /home/cmsusr/.Xauthority does not exist

New 'myvnc:1' desktop is 1df549a6f098:1

Starting applications specified in /home/cmsusr/.vnc/xstartup
Log file is /home/cmsusr/.vnc/1df549a6f098:1.log

[1] 144
VNC connection points:
        VNC viewer address: 127.0.0.1:5901
        HTTP access: http://127.0.0.1:6080/vnc.html
To kill the vncserver enter 'vncserver -kill :1'
</code></pre></div>  </div>

  <p>Open the browser window in the http address given at the start message and connect with the default VNC password <code class="language-plaintext highlighter-rouge">cms.cern</code>. It shows an empty screen to start with and all graphics will pop up there.</p> 
  
  <p>To test, start ROOT by typing <code class="language-plaintext highlighter-rouge">root</code> in the container terminal prompt. In the ROOT prompt, type <code class="language-plaintext highlighter-rouge">TBrowser t</code> to open the ROOT graphical window. If the graphical window opens you are all set and you can exit from ROOT either by choosing the “Quit Root” option from Browser menu of the TBrowser window or by typing <code class="language-plaintext highlighter-rouge">.q</code> in the ROOT prompt.</p>

  <p>Importantly, stop the VNC server before exiting the container. If you don’t do it, you will need to do some cleaning before being able to open the graphics window next time you use the same container. Do the following:</p>

  <div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code> <span class="nb">stop_vnc</span>
 <span class="nb">exit</span>
</code></pre></div>  </div>
</blockquote>

            </article><!-- linux  -->

            <article role="tabpanel" class="tab-pane" id="shell-windows">

<p>We will use the <code class="language-plaintext highlighter-rouge">docker run</code> command to create the container (downloading the appropriate image if it is the first time) and start it right away.</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>docker run -it --name my_od -P -p 5901:5901 -p 6080:6080 -v ${HOME}/cms_open_data_work:/code cmsopendata/cmssw_7_6_7-slc6_amd64_gcc493 /bin/bash
</code></pre></div></div>

<div class="language-plaintext output highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Setting up CMSSW_7_6_7
CMSSW should now be available.
This is a standalone image for CMSSW_7_6_7 slc6_amd64_gcc493.
(/code/CMSSW_7_6_7/src)
</code></pre></div></div>

<p>This is now a bash shell in the CMS open data environment in which you have access to a complete CMS software release that is appropriate for interfacing with the 2015 13 TeV datasets.</p>
              
<p>As there are rate limits for pulls from Docker Hub, you may get the following error message: <code class="language-plaintext highlighter-rouge">docker: Error response from daemon: toomanyrequests: You have reached your pull rate limit. You may increase the limit by authenticating and upgrading.</code>. In that case, try later (the limit is per 6 hours) or use the mirror <code class="language-plaintext highlighter-rouge">gitlab-registry.cern.ch/cms-cloud/cmssw-docker-opendata/cmssw_7_6_7-slc6_amd64_gcc493</code> instead of <code class="language-plaintext highlighter-rouge">cmsopendata/cmssw_7_6_7_vnc</code>.</p>

<blockquote class="testimonial">
  <p>If the docker command exits without giving you the output above, see <a href="https://opendata-forum.cern.ch/t/running-cms-opendata-containers-in-wsl2/30">this post</a> in the CERN Open Data forum (note in particular that the <code class="language-plaintext highlighter-rouge">.wslconfig</code> file that you need to add must not have a file extension, if Windows adds it automatically, rename the file).</p>
</blockquote>

<p>Now let’s understand the options that were used for the <code class="language-plaintext highlighter-rouge">docker run</code> command.</p>

<ul>
  <li>First, the <code class="language-plaintext highlighter-rouge">-it</code> (or <code class="language-plaintext highlighter-rouge">-i</code>) option means to start the container in interactive mode. Essentially, it means that you will end up inside the running container.</li>
  <li>We assign a name to the container using the <code class="language-plaintext highlighter-rouge">--name</code> switch, so that we can refer back to this environment and still access any files we created in there. You can, of course, choose a different name than <code class="language-plaintext highlighter-rouge">my_od</code>.</li>
  <li>The options <code class="language-plaintext highlighter-rouge">-P -p 5901:5901 -p 6080:6080</code> open/publish ports from the container to the local host, needed for the graphical windows</li>
  <li>With <code class="language-plaintext highlighter-rouge">-v ${HOME}/cms_open_data_work:/code</code>, the working directory <code class="language-plaintext highlighter-rouge">cms_open_data_work</code> that you created in your home directory is mounted with the <code class="language-plaintext highlighter-rouge">-v</code> option into the container's <code class="language-plaintext highlighter-rouge">/code</code> directory. This makes it possible to edit files in the CMSSW area of your container with your normal editor on your local computer.</li>
  <li><code class="language-plaintext highlighter-rouge">cmsopendata/cmssw_7_6_7-slc6_amd64_gcc493</code> is the name of the image we will use.  If no label is prepended, Docker assumes that it resides in <a href="https://hub.docker.com/">Docker Hub</a>, the official image repository of Docker.</li>
  <li>Finally, the <code class="language-plaintext highlighter-rouge">/bin/bash</code> option will throw the container into a <code class="language-plaintext highlighter-rouge">bash</code> shell when running interactively.</li>
</ul>

<p>For a more complete listing of options, see <a href="https://docs.docker.com/engine/reference/commandline/container_run/">the official Docker documentation</a> on the <code class="language-plaintext highlighter-rouge">docker run</code> command.</p>

<p>Now, first make sure that you can copy instructions from a browser page to the container terminal. It works in the same manner as the local WSL linux terminal, i.e. you can usually copy from other sources with <code class="language-plaintext highlighter-rouge">Ctrl+C</code> and then paste into your container terminal with mouse right click. Copy from the terminal itself by selecting the text to be copied. If this does not work, you will see later in these instructions how to pass files from your local computer to the container.</p>

<p>This container has a VNC application installed to allow opening graphical windows on a remote machine (seen from the container, your own computer is a remote machine). Start the application with <code class="language-plaintext highlighter-rouge">start_vnc</code> from your container prompt. You will need to start it every time you use the container (if you want to open graphics windows).</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code> start_vnc
</code></pre></div></div>

<div class="language-plaintext output highlighter-rouge"><div class="highlight"><pre class="highlight"><code>xauth:  file /home/cmsusr/.Xauthority does not exist

New 'myvnc:1' desktop is 1df549a6f098:1

Starting applications specified in /home/cmsusr/.vnc/xstartup
Log file is /home/cmsusr/.vnc/1df549a6f098:1.log

[1] 144
VNC connection points:
        VNC viewer address: 127.0.0.1:5901
        HTTP access: http://127.0.0.1:6080/vnc.html
To kill the vncserver enter 'vncserver -kill :1'
</code></pre></div></div>

<p>Open the browser window in the http address given at the start message and connect with the default VNC password <code class="language-plaintext highlighter-rouge">cms.cern</code>. It shows an empty screen to start with and all graphics will pop up there. If it does not open, it may be that the Windows firewall is blocking it. In that case, check <a href="https://opendata-forum.cern.ch/t/windows-firewall-issue/68">these instructions</a>.</p>

<p>To test, start ROOT by typing <code class="language-plaintext highlighter-rouge">root</code> in the container terminal prompt. In the ROOT prompt, type <code class="language-plaintext highlighter-rouge">TBrowser t</code> to open the ROOT graphical window. If the graphical window opens you are all set and you can exit from ROOT either by choosing the “Quit Root” option from Browser menu of the TBrowser window or by typing <code class="language-plaintext highlighter-rouge">.q</code> in the ROOT prompt.</p>

<p>Importantly, stop the VNC server before exiting the container. If you don’t do it, you will need to do some cleaning before being able to open the graphics window next time you use the same container. Do the following:</p>

  <div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code> <span class="nb">stop_vnc</span>
 <span class="nb">exit</span>
</code></pre></div></div>

            </article><!-- Windows  -->


            <article role="tabpanel" class="tab-pane" id="shell-macos">

<p>We will use the <code class="language-plaintext highlighter-rouge">docker run</code> command to create the container (downloading the appropriate image if it is the first time) and start it right away.</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>docker run -it --name my_od -P -p 5901:5901 -p 6080:6080 -v ${HOME}/cms_open_data_work:/code cmsopendata/cmssw_7_6_7-slc6_amd64_gcc493 /bin/bash
</code></pre></div></div>

<div class="language-plaintext output highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Setting up CMSSW_7_6_7
CMSSW should now be available.
This is a standalone image for CMSSW_7_6_7 slc6_amd64_gcc493.
(/code/CMSSW_7_6_7/src)
</code></pre></div></div>

<p>This is now a bash shell in the CMS open data environment in which you have access to a complete CMS software release that is appropriate for interfacing with the 2015 13 TeV datasets.</p>
              
 <blockquote class="testimonial">
  <p> Problems have been reported running amd-based containers such as this on MacOS with M1 chip. Increasing the memory available to Docker may help. Please check the possible solutions in <a href="https://opendata-forum.cern.ch/t/cms-open-data-docker-test-and-validate-error/111/12">this post</a> in the CERN Open Data forum. Note, however, that this may help you to open the container, but it is very likely that problems remain when you try to compile code and run jobs in it.</p> <p>For the CMS open data workshop, we provide a <a href=" http://docker.cms-cloud.net/">temporary solution</a> which gives a docker environment in browser. You can use it for the CMSSW container during the lessons, if needed. Note the following: <ul>
  <li>in the "Play with docker" terminal, after having created the working directory and before starting the container, change the permission of the working directory with <code class="language-plaintext highlighter-rouge">chmod 777 cms_open_data_work</code></li>
  <li>if you use the editor that comes with "Play with docker", the owner of the edited file needs to be changed back in the container with <code class="language-plaintext highlighter-rouge">sudo chown $USER file-name</code></li>
  <li>for the vnc in browser (see below), opens it by cliking "Open port", give 6080 and then add <code class="language-plaintext highlighter-rouge">vnc.html</code> in the URL of the tab that opens.</li></ul>The other containers used in this workshop should run fine on MacOS with M1 chip.</p></blockquote>

<p>As there are rate limits for pulls from Docker Hub, you may get the following error message: <code class="language-plaintext highlighter-rouge">docker: Error response from daemon: toomanyrequests: You have reached your pull rate limit. You may increase the limit by authenticating and upgrading.</code>. In that case, try later (the limit is per 6 hours) or use the mirror <code class="language-plaintext highlighter-rouge">gitlab-registry.cern.ch/cms-cloud/cmssw-docker-opendata/cmssw_7_6_7-slc6_amd64_gcc493</code> instead of <code class="language-plaintext highlighter-rouge">cmsopendata/cmssw_7_6_7-slc6_amd64_gcc493</code>.</p>
              
<p>Now let’s understand the options that were used for the <code class="language-plaintext highlighter-rouge">docker run</code> command.</p>

<ul>
  <li>First, the <code class="language-plaintext highlighter-rouge">-it</code> (or <code class="language-plaintext highlighter-rouge">-i</code>) option means to start the container in interactive mode. Essentially, it means that you will end up inside the running container.</li>
  <li>We assign a name to the container using the <code class="language-plaintext highlighter-rouge">--name</code> switch, so that we can refer back to this environment and still access any files we created in there. You can, of course, choose a different name than <code class="language-plaintext highlighter-rouge">my_od</code>.</li>
  <li>The options <code class="language-plaintext highlighter-rouge">-P -p 5901:5901 -p 6080:6080</code> open/publish ports from the container to the local host, needed for the graphical windows</li>
  <li>With <code class="language-plaintext highlighter-rouge">-v ${HOME}/cms_open_data_work:/code</code>, the working directory <code class="language-plaintext highlighter-rouge">cms_open_data_work</code> that you created in your home directory is mounted with the <code class="language-plaintext highlighter-rouge">-v</code> option into the container's <code class="language-plaintext highlighter-rouge">/code</code> directory. This makes it possible to edit files in the CMSSW area of your container with your normal editor on your local computer.</li>
  <li><code class="language-plaintext highlighter-rouge">cmsopendata/cmssw_7_6_7-slc6_amd64_gcc493</code> is the name of the image we will use.  If no label is prepended, Doc<li>With <code class="language-plaintext highlighter-rouge">-v ${HOME}/cms_open_data_work:/code</code>, the working directory <code class="language-plaintext highlighter-rouge">cms_open_data_work</code> that you created in your home directory is mounted with the <code class="language-plaintext highlighter-rouge">-v</code> option into the container's <code class="language-plaintext highlighter-rouge">/code</code> directory. This makes it possible to edit files in the CMSSW area of your container with your normal editor on your local computer.</li>ker assumes that it resides in <a href="https://hub.docker.com/">Docker Hub</a>, the official image repository of Docker.</li>
  <li>Finally, the <code class="language-plaintext highlighter-rouge">/bin/bash</code> option will throw the container into a <code class="language-plaintext highlighter-rouge">bash</code> shell when running interactively.</li>
</ul>

<p>For a more complete listing of options, see <a href="https://docs.docker.com/engine/reference/commandline/container_run/">the official Docker documentation</a> on the <code class="language-plaintext highlighter-rouge">docker run</code> command.</p>

<p>This container has a VNC application installed to allow opening graphical windows on a remote machine (seen from the container, your own computer is a remote machine). Start the application with <code class="language-plaintext highlighter-rouge">start_vnc</code> from your container prompt. You will need to start it every time you use the container (if you want to open graphics windows).</p>

  <div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>start_vnc
</code></pre></div></div>

<div class="language-plaintext output highlighter-rouge"><div class="highlight"><pre class="highlight"><code>xauth:  file /home/cmsusr/.Xauthority does not exist

New 'myvnc:1' desktop is 1df549a6f098:1

Starting applications specified in /home/cmsusr/.vnc/xstartup
Log file is /home/cmsusr/.vnc/1df549a6f098:1.log

[1] 144
VNC connection points:
        VNC viewer address: 127.0.0.1:5901
        HTTP access: http://127.0.0.1:6080/vnc.html
To kill the vncserver enter 'vncserver -kill :1'
</code></pre></div></div>

<p>Open the browser window in the http address given at the start message and connect with the default VNC password <code class="language-plaintext highlighter-rouge">cms.cern</code>. It shows an empty screen to start with and all graphics will pop up there.</p> 

<p>To test, start ROOT by typing <code class="language-plaintext highlighter-rouge">root</code> in the container terminal prompt. In the ROOT prompt, type <code class="language-plaintext highlighter-rouge">TBrowser t</code> to open the ROOT graphical window. If the graphical window opens you are all set and you can exit from ROOT either by choosing the “Quit Root” option from Browser menu of the TBrowser window or by typing <code class="language-plaintext highlighter-rouge">.q</code> in the ROOT prompt.</p>

<p>Importantly, stop the VNC server before exiting the container. If you don’t do it, you will need to do some cleaning before being able to open the graphics window next time you use the same container. Do the following:</p>

  <div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code> <span class="nb">stop_vnc</span>
 <span class="nb">exit</span>
</code></pre></div></div>

          </article><!-- Mac  -->

        </div> <!-- tab-contents  -->

    </div><!-- nav-tabs  -->
</div><!-- docker-run  -->

## Download the docker images for ROOT and python tools and start container

Containers with ROOT and python libraries installed are provided for your convenience. These containers can be used in the [C++, ROOT and python tools lesson](https://cms-opendata-workshop.github.io/workshop2022-lesson-cpp-root-python/) and later on for your work with CMS open data.

### ROOT container

ROOT is included in the CMSSW container, but it is an old version because it needs to be compatible with the environment needed to access CMS open data AOD and MiniAOD files. In this tutorial, and in your work with CMS open data, you will often work on data that have been derived from the AOD or MiniAOD files and are not tied to a specific ROOT version. Therefore, a container with more recent ROOT version is provided. 

First, create a working directory on your local computer:

~~~
cd
mkdir cms_open_data_root
~~~
{: .language-bash}

Then, download [the ROOT container](https://gitlab.cern.ch/cms-cloud/root-vnc) and start it with the `docker run` command.

If you are on native Linux and want to use X11-forwarding, use

~~~
docker run -it --name my_root --net=host --env="DISPLAY" -v $HOME/.Xauthority:/home/cmsusr/.Xauthority:rw -v ${HOME}/cms_open_data_root:/code gitlab-registry.cern.ch/cms-cloud/root-vnc:latest
~~~
{: .language-bash}

On MacOS and Windows WSL2 (and on native Linux if you do not want to use X11-forwarding), use

~~~
docker run -it --name my_root -P -p 5901:5901 -p 6080:6080 -v ${HOME}/cms_open_data_root:/code gitlab-registry.cern.ch/cms-cloud/root-vnc:latest
~~~
{: .language-bash}


This opens a bash shell where you can type your commands. Edit files in the `cms_open_data_root` directory on your local computer, but run the commands in the container.

For graphics, on native Linux, use X11-forwarding. On other systems, use VNC that is installed in the container and start the graphics windows with `start_vnc`. Open the browser window in the address given at the start message ([http://127.0.0.1:6080/vnc.html](http://127.0.0.1:6080/vnc.html)) with the default VNC password is `cms.cern`. It shows an empty screen to start with and all graphics will pop up there.

Type `exit` to leave the container, and if you have started VNC, stop it first:

~~~
stop_vnc
exit
~~~
{: .language-bash}


### Python tools container

ROOT is not the only option for analysis of CMS open data. A container image is provided with all python libraries that will be needed in this tutorial.

First, create a working directory on your local computer:

~~~
cd
mkdir cms_open_data_python
~~~
{: .language-bash}

Then, download [the python container](https://gitlab.cern.ch/cms-cloud/python-vnc) and start it with the `docker run` command.

If you are on native Linux and want to use X11-forwarding, use

~~~
docker run -it --name my_python -P -p 8888:8888 --net=host --env="DISPLAY" -v $HOME/.Xauthority:/home/cmsusr/.Xauthority:rw -v ${HOME}/cms_open_data_python:/code gitlab-registry.cern.ch/cms-cloud/python-vnc:latest
~~~
{: .language-bash}

On MacOS and Windows WSL2 (and on native Linux if you do not want to use X11-forwarding), use

~~~
docker run -it --name my_python -P -p 5901:5901 -p 6080:6080 -p 8888:8888 -v ${HOME}/cms_open_data_python:/code gitlab-registry.cern.ch/cms-cloud/python-vnc:latest
~~~
{: .language-bash}


This opens a bash shell where you can type your commands. Edit files in the `cms_open_data_python` directory on your local computer, but run the commands in the container.

You can run jupyter notebooks in this container by typing in the container prompt

~~~
jupyter-lab --ip=0.0.0.0 --no-browser
~~~
{: .language-bash}

and opening the link in the message on your browser.

> If you see `Permission denied` when you try to open a new notebook, you most likely forgot to create the local working directory before creating the container. In that case, the directory was created automatically but with the wrong user/group. Exit from the container with `exit`. Then remove the container, remove the working directory, create it again:
> ~~~
> docker rm my_python
> rm -rf cms_open_data_python
> mkdir cms_open_data_python
> ~~~
> {: .language-bash}
> and create the container again with the `docker run ...` command above.
{: .testimonial}

For other graphics, on native Linux, use X11-forwarding. On other systems, use VNC that is installed in the container and start the graphics windows with `start_vnc`. Open the browser window in the address given at the start message ([http://127.0.0.1:6080/vnc.html](http://127.0.0.1:6080/vnc.html)) with the default VNC password is `cms.cern`. It shows an empty screen to start with and all graphics will pop up there.

Type `exit` to leave the container, and if you have started VNC, stop it first:

~~~
stop_vnc
exit
~~~
{: .language-bash}

## Coming back to the same container

You can come back to the same container you've used earlier with the ```docker start ...``` command. 
 
~~~
docker start -i my_od
~~~
{: .language-bash}

 Note that running the ```docker run ...``` command as before would create a new container from the image you've downloaded. This would be a new environment. However, as we are mounting the directory from the local computer into the container, you will see the files from your earlier container even in your new container. Most often, you do not want to create a new container but you would use the existing container to go to the same working area with all our files and code saved.


> ## CHALLENGE! Test persistence
>
> Go into the container and in the `/code/CMSSW_7_6_7/src` directory, create a test file using some
> simple shell commands. Type the following exactly as you see it.
> It will dump some text into a file and then print the contents
> of the file to the screen
> ~~~
> echo "I am still here" > test.tmp
> cat test.tmp
>
> ~~~
> {: .language-bash}
>
> After you've done this, check if you see the file `test.tmp` in your local computer in the `cms_open_data_work/CMSSW_7_6_7/src` directory.
> If you did it correctly, you should be able to list the contents
> of the directory with ```ls -l``` and see your file from before!
> If not, check that you followed all the instructions
> above correctly or contact the facilitators.
>
> Now, exit from the container and remove it with
> ~~~
> docker rm my_od
> ~~~
> {: .language-bash}
>
> Create a new container with the `docker run` command that you used in the first place.
> Check if you see the file that you created before.
>
> Note that with the volume mount, your files will not disappear when you remove the container because they are stored in a directory on the local computer. If you really want to get rid of them, you will have to delete them either on the container or on your local computer.
>
> You can make use of this, for example, when you have forgotten to stop VNC with `stop_vnc` when you exit the container. Probably the quickest way to clean is to remove and recreate the container. When you do it, the files that block the VNC from starting will be removed and as they are not located in the mounted directory, they will not be present when you create a new container. But the files in your working area (as `test.tmp` above) will be there again.
{: .challenge}


## Stopping and removing containers

As you are learning how to use Docker, you may find yourself with multiple containers. Or maybe
you started a container with your favourite name with some set of flags and now you want use that same name but with new flags. In that case, you will want to stop the container and remove it.

A container stops when you type the ```exit``` command in the container prompt. It may happen that you accidentally close the terminal where the container is running. In that case, the container will not stop and it will remain running. You can list the running containers with ```docker ps```. You can either return to the container using its name (here "my_od") with the ```start``` command on your local machine and then exit normally from the container prompt:

~~~
docker start -i my_od
exit
~~~
{: .language-bash}

or **stop** the container with

~~~
docker stop my_od
~~~
{: .language-bash}

To stop **all** running containers:

~~~
docker stop $(docker ps -q)
~~~
{: .language-bash}

To **remove** the container "my_od", you would type the following. Note that this will delete the container and all files, but the files in the `CMSSW_7_6_7/src` directory which is shared with your local computer will remain in your local computer's directory.

~~~
docker rm my_od
~~~
{: .language-bash}

To remove **all** containers:
~~~
docker rm $(docker ps -aq)
~~~
{: .language-bash}

> ## Don't worry!
> Note that these commands *will not* remove the actual Docker *image* that you downloaded and may have taken
> quite some time to download! Whew!
>
{: .callout}


{% include links.md %}
