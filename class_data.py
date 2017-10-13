# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 02:30:51 2017

@author: heeju
"""

import os

## 다수의 fna 집합 -> lrn, names -> bm, umx, wts, cls로 진행되는 일련의 data
## (status : 1 -> 2 -> 3단계)
class Data:
    
    ## fna 파일 로드
    def __init__ (self, count, *fileList):
        ## fna 파일 갯수
        self.count = count
        ## fna 파일 경로
        self.fileList = {}
        ## 지워진 파일 이름
        self.delfileList = []
        
        if (fileList.index != 0):
            for f in fileList:
                self.fileList[os.path.splitext(f)[1]] = f
                
            ## fna 파일 로드 완료
            self.status = 1
        else:
            ## fna 파일 로드 실패
            self.status = 0
            
        
    ## 현재 data 상태 반환
    def getStatus(self):
        return self.status
    
    ####---------------------------------------------
    ## content slicer(5000개 유전자씩)
    def split(self, content, split_size = 5000):
        def _f(c, split_size):
            while c:
                yield c[:split_size]
                c = c[split_size:]
        return list(_f(content, split_size))
    
    ## content window(4개 유전자씩)
    def window(self, content, window_size = 4):
        for i in range(len(content) - window_size):
            yield content[i : i + window_size]
    ####----------------------------------------------
    
    ## lrn, names로 변환
    def convertTOlrn(self, projectName):
        ## fna 파일 로드 완료 상태
        if (self.getStatus() >= 1):
            dataTOlrn = ""
            dataTOnames = ""
            
            ## 136개 tetranucleotide
            dic = {'AAAA':0,'AAAT':0,'AAAC':0,'AAAG':0,'AATA':0,'AATT':0,'AATC':0,'AATG':0,
                   'AACA':0,'AACT':0,'AACC':0,'AACG':0,'AAGA':0,'AAGT':0,'AAGC':0,'AAGG':0,
                   'ATAA':0,'ATAT':0,'ATAC':0,'ATAG':0,'ATTA':0,'ATTC':0,'ATTG':0,'ATCA':0,
                   'ATCT':0,'ATCC':0,'ATCG':0,'ATGA':0,'ATGT':0,'ATGC':0,'ATGG':0,'ACAA':0,
                   'ACAC':0,'ACAG':0,'ACTA':0,'ACTC':0,'ACTG':0,'ACCA':0,'ACCT':0,'ACCC':0,
                   'ACCG':0,'ACGA':0,'ACGT':0,'ACGC':0,'ACGG':0,'AGAA':0,'AGAC':0,'AGAG':0,
                   'AGTA':0,'AGTC':0,'AGTG':0,'AGCA':0,'AGCT':0,'AGCC':0,'AGCG':0,'AGGA':0,
                   'AGGC':0,'AGGG':0,'TAAA':0,'TAAC':0,'TAAG':0,'TATA':0,'TATC':0,'TATG':0,
                   'TACA':0,'TACC':0,'TACG':0,'TAGA':0,'TAGC':0,'TAGG':0,'TTAA':0,'TTAC':0,
                   'TTAG':0,'TTTC':0,'TTTG':0,'TTCA':0,'TTCC':0,'TTCG':0,'TTGA':0,'TTGC':0,
                   'TTGG':0,'TCAC':0,'TCAG':0,'TCTC':0,'TCTG':0,'TCCA':0,'TCCC':0,'TCCG':0,
                   'TCGA':0,'TCGC':0,'TCGG':0,'TGAC':0,'TGAG':0,'TGTC':0,'TGTG':0,'TGCA':0,
                   'TGCC':0,'TGCG':0,'TGGC':0,'TGGG':0,'CAAC':0,'CAAG':0,'CATC':0,'CATG':0,
                   'CACC':0,'CACG':0,'CAGC':0,'CAGG':0,'CTAC':0,'CTAG':0,'CTTC':0,'CTCC':0,
                   'CTCG':0,'CTGC':0,'CTGG':0,'CCAC':0,'CCTC':0,'CCCC':0,'CCCG':0,'CCGC':0,
                   'CCGG':0,'CGAC':0,'CGTC':0,'CGCC':0,'CGCG':0,'CGGC':0,'GAAC':0,'GATC':0,
                   'GACC':0,'GAGC':0,'GTAC':0,'GTCC':0,'GTGC':0,'GCCC':0,'GCGC':0,'GGCC':0}
            
            ## 여러 개의 fna data를 하나의 lrn, names에 저장
            dataTOlrn += "%Key\t"
            for tetnu in dic.keys():
                dataTOlrn += tetnu + "\t"
            dataTOlrn += "\n"
                        
            ## 전체 contig 개수
            dataNum = 0
            for f in self.fileList:
                with open(f, 'r') as complete:
                    name = complete.readline()
                    content = complete.read()
                    ## 파일 별 contig 개수
                    contigNum = 0
                    tetnuNum = 0
                    
                    ## 5000개 씩의 split contig마다 lrn과 names에 한 줄 씩 추가
                    for contig in self.split(content, 5000):
                        for tetnu in self.window(contig, 4):
                            if (tetnu in dic):
                                tetnuNum += 1
                                
                                dic[tetnu] += 1
                        
                        contigNum += 1
                        dataNum += 1
                        dataTOlrn += "%d\t" % dataNum
                        for tetnu in dic.keys():
                            dataTOlrn += "%lf\t" % ( dic[tetnu] / tetnuNum )
                            ## dic 초기화
                            dic[tetnu] = 0
                        dataTOlrn += "\n"
                        
                        dataTOnames += "%d\t" % dataNum + name[1:-1] + "_%d\n" % contigNum
                        
                        ## tetnuNum 초기화
                        tetnuNum = 0
            
            with open(projectName + '.lrn', 'w') as lrn:
                lrn.write("#" + projectName + "\n")
                lrn.write("%" + "%d\n" % dataNum)
                lrn.write("%" + "%d\n" % 137)
                lrn.write(dataTOlrn)
                
            with open(projectName + '.names', 'w') as names:
                names.write("#" + projectName + "\n")
                names.write("%" + "%d\n" % dataNum)
                names.write(dataTOnames)
                        
            ## lrn, names로 변환 완료
            self.status = 2
            return 0
        
        ## fna 파일 로드 실패 상태
        elif (self.getStatus() == 0):
            return -1
            
                
                
#data = Data(2, 'GCF_000005845.2_ASM584v2_genomic.fna', 'contig0.fna')
#data.convertTOlrn('dd')