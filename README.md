This repository contains a Proof of Concept exploit of the Estonian ID software DigiDoc4 version 25.5/25.6
On August 20th 2025, RIA released the version 25.8 of the DigiDoc4 software. The release notes of this update mentioned "Improved digital signature validation" as a major change (https://www.id.ee/en/article/id-software-versions-info-release-notes/). This poses the question: "What was improved and what could have been the initiator for the update?"

As my final thesis in I am analysing this update and trying to come up with a Proof of Concept exploit.
Thus far I have managed to exploit it to the point, to where in a signed ASiCE container, the document to which the signature was given, can be modified or replaced, without changing the validity seen in the DigiDoc4 appication.

Below is a description, of how this was achieved in x steps:

1. Assume that you have a digitally signed container, in our case let that container be original.asice, which was signed by me and contains the file original.txt
<img width="1918" height="1120" alt="image" src="https://github.com/user-attachments/assets/834d1679-aaf8-4c1f-a196-997fdbe53f99" />

2. This container can be unpacked into the following files using the unpack_asice.py script:
 ~~~text
\original.txt
\mimetype
\META-INF\manifest.xml
\META-INF\signatures0.xml
 ~~~

3. The exploit lies in the fact that anyone could open the signatures0.xml file in a text editor and replace all the following elements with empty strings:
* ds:CanonicalizationMethod Algorithm=
* ds:SignatureMethod Algorithm=
* ds:DigestMethod Algorithm=

And also empty out all the <ds:DigestValue></ds:DigestValue> elements in the signature

This modification passed the validation checks, because the higher level validation methods expected the exceptions thrown in the lower levels to have an e.cause(), which they did not. So with the update this vulnerability was fixed.

4. Upon clearing out these values in the signatures0.xml, the attacker only has to modify or replace the document to which the signature was given. If they decide to replace it, then they would also need to replace the file name in mainfest.xml, and in the case of our exploit, also in original_file_order.txt.

5. After changing all these values, the attacker can repack the container with repack_asice.py, and it will still be valid in the 25.5/25.6 version of the software.

   <img width="1914" height="1122" alt="image" src="https://github.com/user-attachments/assets/2be68008-1763-4dc0-a6a4-a76eef05e30a" />


