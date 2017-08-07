# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 14:08:32 2017

@author: heeju
"""

## Data를 생성, 관리하기 위한 대단위
## 프로젝트 생성(폴더) -> fna 파일 추가 -> 저장으로 진행
## (status : 1 -> 2 -> 3단계)
class Project:
    
    def __init__ (self, name, path):
        ## 프로젝트 이름
        self.name = name
        ## 프로젝트 경로
        self.path = path
        
        ## 프로젝트 폴더 생성 완료
        self.status = 1
        
    ## 현재 프로젝트 상태 반환
    def getStatus(self):
        return self.status
        
    ####---------------------------------------------
    ## fna 파일 리스트 추가
    def addFna():
        break
    