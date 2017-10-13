# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 14:08:32 2017

@author: heeju
"""

import class_data as datas

import os

## Data를 생성, 관리하기 위한 대단위
## 프로젝트 생성 -> fna, fasta 파일 변경됨 -> 저장으로 진행
## (status : 1 -> 2 -> 3단계)
class Project():
    
    def __init__ (self, name, path, new):
        ## 프로젝트 이름
        self.name = name
        ## 프로젝트 경로
        self.path = path
        ## 프로젝트 데이터
        self.data = datas.Data(0)
        
        if new:
            ## 프로젝트 생성
            self.status = 1
        else:
            ## 프로젝트 로드
            self.status = 3
        
        
    ####---------------------------------------------
    ## fna, fasta 파일 리스트 추가하여 변경됨
    def addFiles(self, names):
        for f in names:
            if ((os.path.splitext(f)[1][1:]) == ('fna' or 'fasta')):
                # 동일한 이름의 파일은 제외
                if (not os.path.basename(f) in self.data.fileList):
                    self.data.fileList[os.path.basename(f)] = f;
        
        self.status = 2
        
    ## fna, fasta 파일 삭제되어 변경됨
    def deleteFile(self, name):
        del self.data.fileList[name];
        self.data.delfileList.append(name);
        
        self.status = 2
    
    ####---------------------------------------------
    ## 저장
    def saved(self):
        self.status = 3
        
    ####---------------------------------------------
    ## 로드 시 오류(저장 필요)
    def wrongLoaded(self):
        self.status = 2
        
    ####---------------------------------------------    
    ## 현재 프로젝트 상태 반환
    def getStatus(self):
        return self.status