This repository contains a Proof of Concept exploit of the Estonian ID software DigiDoc4 version 25.5/25.6
On August 20th 2025, RIA released the version 25.8 of the DigiDoc4 software. The release notes of this update mentioned "Improved digital signature validation" as a major change (https://www.id.ee/en/article/id-software-versions-info-release-notes/). This poses the question: "What was improved and what could have been the initiator for the update?"

As my final thesis in I am analysing this update and trying to come up with a Proof of Concept exploit.
Thus far I have managed to exploit it to the point, to where in a signed ASiCE container, the document to which the signature was given, can be modified or replaced, without changing the validity seen in the DigiDoc4 appication.

Below is a description, of how this was achieved in x steps:

1. Assume that you have a digitally signed container, in our case let that container be original.asice, which was signed by me and contains the file original.txt

2. This container can be unpacked into the following files using the unpack_asice.py script:

\original.txt
\mimetype
\META-INF\manifest.xml
\META-INF\signatures0.xml

