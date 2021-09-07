from dahuffman import HuffmanCodec
import filecmp
import os

#consts
inputFilePath = "./input/soup.bmp"
inputPathSplit = inputFilePath.split("/")
lz77CodePath = "./output/" + inputPathSplit[-1] + ".lz77"
lz77ImagePath = "./output/" + "(lz77)" + inputPathSplit[-1]
huffCodePath = "./output/" + inputPathSplit[-1] + ".huf"
huffImagePath = "./output/" + "(huff)" + inputPathSplit[-1]

dictBufSize = 31 * 1
inputBufSize = 32 * 1

showSteps = False

def lz77Match(dictBuf, inp):
    if len(dictBuf) == 0:
        return [0,0]
    dictLen = len(dictBuf)
    word = dictBuf + inp[:-2]
    resultWord = inp[:-1]
    while len(resultWord) > 0:
        if resultWord in word:
            #print(dictLen - word.find(resultWord), len(resultWord))
            return [dictLen - word.find(resultWord), len(resultWord)]
        resultWord = resultWord[:-1]
        word = word[:-1]
    #print("0, 0")
    return [0, 0]

def lz77Kod(word, n, m, showSteps):
    resultCode = []
    curIndex = 0
    if m > len(word):
        inpBuf = word[0:]
    else:
        inpBuf = word[0:m]
    dicBuf = []
    if showSteps:
        print(dicBuf, end=" ")
        print(inpBuf, end=" ")
    while curIndex < len(word):
        match = lz77Match(dicBuf, inpBuf)
        if curIndex + match[1] + 1 < len(word):
            curIndex += match[1] + 1
        else: curIndex = len(word)
        #inpBuf change
        if curIndex + m <= len(word):
            inpBuf = word[curIndex: curIndex + m]
        else:
            inpBuf = word[curIndex:]
        if curIndex - n < 0:
            dicBuf = word[:curIndex]
        else:
            dicBuf = word[curIndex - n:curIndex]
        match.append(word[curIndex - 1])
        resultCode.append(match)
        if showSteps: print(resultCode[len(resultCode) - 1])
        if showSteps:
            if(len(inpBuf)) > 0:
                print(dicBuf, end=" ")
                print(inpBuf, end=" ")
    return resultCode

def lz77Dekod(code, showSteps):
    result = bytearray()
    for element in code:
        if element[1] == 0:
            result.append(element[2])
        else:
            indexStart = len(result) - element[0]
            if element[1] > element[0]:
                n = element[1] // element[0]
                r = element[1] % element[0]
                table = result[indexStart:]
                for i in range(n):
                    for byteItem in table:
                        result.append(byteItem)
                for byteItem in table[:r]:
                    result.append(byteItem)
            else:
                indexEnd = len(result) - element[0] + element[1]
                for byteItem in result[indexStart:indexEnd]:
                    result.append(byteItem)
            result.append(element[2])
        if showSteps: print(result)
    return result

def convToStr(list):
    result = []
    for element in list:
        result.append(str(element[0]) + "|" + str(element[1]) + "|" + hex(element[2]))
    return result

def convToList(list):
    result = []
    for element in list:
        elementSplit = element.split("|")
        result.append([int(elementSplit[0]), int(elementSplit[1]), int(elementSplit[2], 16)])
    return result

#encode
file = open(inputFilePath, "rb")
inputData = file.read()
file.close()

#lz77 Huffman
code = convToStr(lz77Kod(inputData, dictBufSize, inputBufSize, showSteps))
codec = HuffmanCodec.from_data(code)
encoded = codec.encode(code)


#write lz77 + huff code
fileOutput = open(lz77CodePath, "wb")
fileOutput.write(encoded)

fileOutput.close()

#decode lz77 + huff
fileInput = open(lz77CodePath, "rb")
bytes = fileInput.read()
fileInput.close()

filelz77Dekod = open(lz77ImagePath, "wb")
filelz77Dekod.write(lz77Dekod(convToList(codec.decode(bytes)), showSteps))
filelz77Dekod.close()

#porównanie plików
print("comp file: " + inputFilePath + ", with: " + lz77ImagePath + " " + str(filecmp.cmp(inputFilePath, lz77ImagePath)))

#Huffman test

codecHuf = HuffmanCodec.from_data(inputData)

encodedHuf = codecHuf.encode(inputData)

#save huffman code
fileEncodedHuf = open(huffCodePath, "wb")
fileEncodedHuf.write(encodedHuf)
fileEncodedHuf.close()

#read huffman file
fileEncodedInputHuf = open(huffCodePath, "rb")

#get image from huffman code
fileHuf = open(huffImagePath, "wb")
fileHuf.write(codecHuf.decode(fileEncodedInputHuf.read()))
fileEncodedInputHuf.close()
fileHuf.close()

#porównanie plików
print("comp file: " + inputFilePath + ", with: " + huffImagePath + " " + str(filecmp.cmp(inputFilePath, huffImagePath)))

#porównanie rozmiarów i stopnia kompresji
hufSize = os.path.getsize(huffCodePath)
lz77hufSize = os.path.getsize(lz77CodePath)
originSize = os.path.getsize(inputFilePath)
print("----------------------")
print("Original:\n size: " + str(originSize) + " bytes\n"
      "Huffman:\n size: " + str(hufSize) + " bytes, compression: " + str(round((hufSize)/originSize * 100, 2)) + "%\n"
      "Lz77 + Huffman:\n size: " + str(lz77hufSize) + " bytes, compression: " + str(round((lz77hufSize)/originSize * 100, 2)) + "%\n"
      "Lz77 ([huf - lz77huf]/huf):\n compression: " + str(round((hufSize - lz77hufSize)/hufSize * 100, 2)) + "%")
