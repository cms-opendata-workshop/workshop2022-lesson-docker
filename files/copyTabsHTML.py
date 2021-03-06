#!/usr/bin/env python

#This is a script to copy the HTML code generated by the
#os_instructions_source.md file in the _site/os_instructions_source.html
#file to the appropriate section in the _episodes/03-docker-for-cms-opendata.md file
#The scrip assumes one is at the top of the lesson repository
import os

HTMLSRCFILE = "_site/os_instructions_source.html"
MDDIRFILE = "_episodes/03-docker-for-cms-opendata.md"
MDFILE = MDDIRFILE.split("/")[1]

CLEANMDFILE = "03-docker-for-cms-opendata.md_clean"
NEWMDFILE = "03-docker-for-cms-opendata.md_new"

DOWNDIV = '<div id="docker-run">'
MNTDIV = '<div id="docker-run-with-mount">'

#download article (DA) limit
LX_DA= '<article role="tabpanel" class="tab-pane active" id="shell-linux">'
WX_DA = '<article role="tabpanel" class="tab-pane" id="shell-windows">'
MAC_DA = '<article role="tabpanel" class="tab-pane" id="shell-macos">'
#artile limit
AL = '</article>'

#mount article (MA) limit
LX_MA= '<article role="tabpanel" class="tab-pane active" id="shell-linux-mnt">'
WX_MA = '<article role="tabpanel" class="tab-pane" id="shell-windows-mnt">'
MAC_MA = '<article role="tabpanel" class="tab-pane" id="shell-macos-mnt">'

#source file limit pairs, which encapsulate the corresponding sections (download or mounting) with hmtl 
LX_Dlim = ['<h3 id="downloading-and-start">Downloading and start</h3>','<h3 id="mounting-a-local-volume-example">Mounting a local volume example</h3>']
LX_Mlim = ['<h3 id="mounting-a-local-volume-example">Mounting a local volume example</h3>','<h2 id="windows-instructions">Windows instructions</h2>']
WX_Dlim = ['<h3 id="downloading-and-start-1">Downloading and start</h3>','<h3 id="mounting-a-local-volume-example-1">Mounting a local volume example</h3>']
WX_Mlim = ['<h3 id="mounting-a-local-volume-example-1">Mounting a local volume example</h3>','<h2 id="mac-os-instructions">Mac-OS instructions</h2>']
MAC_Dlim = ['<h3 id="downloading-and-start-2">Downloading and start</h3>','<h3 id="mounting-a-local-volume-example-2">Mounting a local volume example</h3>']
MAC_Mlim = ['<h3 id="mounting-a-local-volume-example-2">Mounting a local volume example</h3>','</article>']



########################################################################
def clean_md_file():
########################################################################
    writeme = True
    cleanfile = open(CLEANMDFILE,"a")

    with open(MDDIRFILE, 'r') as fd:
        contents = fd.readlines()
        for line in contents:
            if LX_DA in line or LX_MA in line or WX_DA in line or WX_MA in line or MAC_DA in line or MAC_MA in line:
                cleanfile.write(line)
                writeme = False
            if (writeme == False) and (AL in line):
                cleanfile.write(line)
                writeme = True
            else:
                if writeme: cleanfile.write(line)
            
    cleanfile.close()

###########################################################
def fill_out_html(line,tlimits,newfile):
###########################################################
    hcontent = open(HTMLSRCFILE,"r").readlines()
    writehtml = False
    for hline in hcontent:
        if tlimits[0] in hline:
            writehtml = True
            continue
        if (writehtml==True) and (tlimits[1] not in hline):
            newfile.write(hline)
        else:
            writehtml = False

    return newfile
            
#######################################################
def copy_hmtl_to_md():
#######################################################
    newfile = open(NEWMDFILE,"a")
    isArticle = False
    
    with open(CLEANMDFILE,'r') as cf:
        contents = cf.readlines()
        for line in contents:
            if LX_DA in line:
                newfile.write(line)
                isArticle = True
                newfile = fill_out_html(line,LX_Dlim,newfile)
            if LX_MA in line:
                newfile.write(line)
                isArticle = True
                newfile = fill_out_html(line,LX_Mlim,newfile)
            if WX_DA in line:
                newfile.write(line)
                isArticle = True
                newfile = fill_out_html(line,WX_Dlim,newfile)
            if WX_MA in line:
                newfile.write(line)
                isArticle = True
                newfile = fill_out_html(line,WX_Mlim,newfile)
            if MAC_DA in line:
                newfile.write(line)
                isArticle = True
                newfile = fill_out_html(line,MAC_Dlim,newfile)
            if MAC_MA in line:
                newfile.write(line)
                isArticle = True
                newfile = fill_out_html(line,MAC_Mlim,newfile)                
            if (isArticle == True) and (AL in line):
                newfile.write(line)
                isArticle = False
            else:
                if not isArticle: newfile.write(line)

    newfile.close()

    os.system('mv '+NEWMDFILE+" "+MDDIRFILE)
    os.system('rm -r '+CLEANMDFILE)
            
    
        
        

    
#######################################################
if __name__ =='__main__':
#######################################################

    if not os.path.exists(HTMLSRCFILE):
        print ("File "+HTMLSRCFILE+" doesn't exist.")
        exit(1)
    if not os.path.exists(MDDIRFILE):
        print ("File "+MDDIRFILE+" doesn't exist.")
        exit(1)

    #erase tmp files
    os.system("rm -f "+CLEANMDFILE)
    os.system("rm -f "+NEWMDFILE)
    
    #make safety copy first
    #os.system ("cp "+MDDIRFILE+" files/"+MDFILE+"_back")

    #clean the md file first
    clean_md_file()

    #write new html to clean file
    copy_hmtl_to_md()
    


