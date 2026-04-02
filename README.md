This repository contains a Proof of Concept exploit of the Estonian ID software DigiDoc4 version 25.5/25.6
On August 20th 2025, RIA released the version 25.8 of the DigiDoc4 software. The release notes of this update mentioned "Improved digital signature validation" as a major change (https://www.id.ee/en/article/id-software-versions-info-release-notes/). This poses the question: "What was improved and what could have been wrong prior to the update?" The next day, August 21st, a news article was published in digigeenius (https://geenius.delfi.ee/artikkel/120451500/ria-soovitab-inimestel-varskendada-id-tarkvara-kuid-jaab-uuenduse-tagamaid-selgitades-napisonaliseks). And on August 22nd, a similar article was also published on www.id.ee (https://www.id.ee/en/article/ria-soovitab-kasutajatel-uuendada-id-tarkvara-eng/).

As my thesis in I am analysing this update and trying to come up with a Proof of Concept exploit.
Thus far I have managed to exploit it to the point, to where in a signed ASiCE container, the document to which the signature was given, can be modified or replaced, without changing the validity seen in the DigiDoc4 appication.

Below is a description, of how this was achieved in the following steps, using the files in this repo and assuming you are using Windows to test out the .exe files:

1. Assume that you have a digitally signed container, in our case let that container be original.asice, which was signed by me and contains the file original.txt
<img width="1918" height="1120" alt="image" src="https://github.com/user-attachments/assets/834d1679-aaf8-4c1f-a196-997fdbe53f99" />

<img width="1915" height="1128" alt="image" src="https://github.com/user-attachments/assets/dd83e01a-1d8e-46c4-a073-38a9827f546d" />


2. This container can be unpacked into the following files using the unpack_asice.py script:
 ~~~text
\original.txt
\mimetype
\META-INF\manifest.xml
\META-INF\signatures0.xml
 ~~~

3. The exploit lies in the fact that anyone could open the signatures0.xml file in a text editor and replace all the following elements with empty or modified strings:
* ds:CanonicalizationMethod Algorithm=
* ds:SignatureMethod Algorithm=
* ds:DigestMethod Algorithm=

And also empty out or modify all the <ds:DigestValue></ds:DigestValue> elements in the signature

This modification passed the validation checks, because the higher level validation methods expected the exceptions thrown in the lower levels to have an e.cause(), which they did not. So with the update this vulnerability was fixed. The fix can be inspected here: https://github.com/open-eid/libdigidocpp/pull/690/changes

4. Upon clearing out these values in the signatures0.xml, the attacker only has to modify or replace the document to which the signature was given. If they decide to replace it, then they would also need to replace the file name in mainfest.xml, and in the case of our exploit, also in original_file_order.txt.

5. After changing all these values, the attacker can repack the container with repack_asice.py, and it will still be valid in the 25.5/25.6 version of the software.

<img width="1914" height="1122" alt="image" src="https://github.com/user-attachments/assets/2be68008-1763-4dc0-a6a4-a76eef05e30a" />

On the below image the user could notice, that the Signature method is missing due to an empty string

<img width="1917" height="1129" alt="image" src="https://github.com/user-attachments/assets/9b646541-0c18-45c1-ac49-93ac918be56e" />

But this can be "fixed" by just simply replacing the ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsigEXPLOIT" or any other value with the prefix "http://www.w3.org/2001/04/xmldsig"

<img width="1918" height="1128" alt="image" src="https://github.com/user-attachments/assets/08a47199-b0a8-4d5c-8ae1-970aa1391806" />

So all values that are visible to the regular user remain the same, while the signed document was changed.


Below are screenshots that successfully display the modified container as having an invalid signature in the updated version:

<img width="1918" height="1126" alt="image" src="https://github.com/user-attachments/assets/22769ded-6825-40c3-b102-f4e20cfdda46" />

<img width="1914" height="1123" alt="image" src="https://github.com/user-attachments/assets/e3910423-70fe-4b58-a836-fb3c009574c6" />


