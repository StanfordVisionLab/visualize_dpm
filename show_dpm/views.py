from django.shortcuts import render_to_response, get_object_or_404 
import sys 
sys.path.append('/imagenetdb/tgebru/') 
from mysql_utils import connect_to_db

num_ims=1000
num_training_data=1000
num_parts=8
num_components=3
threshold=0
root='/afs/cs.stanford.edu/u/tgebru/cars/code/dpm/'
image_ids=root+'im_ids_%d.txt'%(num_ims)
image_paths=root+'im_paths_%d.txt'%(num_ims)
gt_bbox_file=root+'bboxes_%d.txt'%(num_ims)
#dpm_bbox_file=root+'dpm_bboxes_%d.txt'%(num_ims)
#detected_dpm_bbox_file=root+'detected_dpm_bboxes_%d.txt'%(num_ims)

default=True
if default:
  dpm_bbox_file=root+'dpm_bboxes/default_%d_%d_%d.txt'%(num_ims,num_parts,num_components)
  detected_dpm_bbox_file=root+'dpm_bboxes/detected_dpm_default_%d_%d_%d.txt'%(num_ims,num_parts,num_components)
else:
  dpm_bbox_file='%sdpm_bboxes/%d_%d_%d_%d_%d.txt'%(root,num_ims,num_training_data,num_parts,num_components,threshold)
  detected_dpm_bbox_file='%sdpm_bboxes/detected_dpm_%d_%d_%d_%d_%d.txt'%(root,num_ims,num_training_data,num_parts,num_components,threshold)

def get_bboxes(filename):
  gt_bboxes=open(filename,'r').read().split('\n')
  im_ids=get_imids()
  i=0
  im_bboxes=[]
  bboxes={}
  for b in gt_bboxes:
    if 'end' not in b:
      im_bboxes.append(b)
    else: 
      bboxes[int(im_ids[i])]=im_bboxes
      im_bboxes=[]
      i += 1

  return bboxes

def make_bbox_dict(bbox_list):
  bboxes=[]
  for b in bbox_list:
    bbox={}
    boxes=b.split('\t')
    bbox['x1']=boxes[0]
    bbox['y1']=boxes[1]
    bbox['x2']=boxes[2]
    bbox['y2']=boxes[3]
    bboxes.append(bbox)
  
  return bboxes
  
def get_bbox_dict(imid):
  gt_bboxes=get_bboxes(gt_bbox_file)
  dpm_bboxes=get_bboxes(dpm_bbox_file)
  detected_dpm_bboxes=get_bboxes(detected_dpm_bbox_file)
  gt=gt_bboxes[imid]
  dpm=dpm_bboxes[imid]
  detected_dpm=detected_dpm_bboxes[imid]
  gt_dict=make_bbox_dict(gt)
  dpm_dict=make_bbox_dict(dpm)
  detected_dpm_dict=make_bbox_dict(detected_dpm)
  return gt_dict,dpm_dict,detected_dpm_dict
  
def get_imids():
  return(open(image_ids,'r').read().split('\n'))

def index(request):
  imids=get_imids
  return render_to_response('show_dpm/index.html', {'imids':imids})

def show_pic(request,imid):
  im_int=int(imid)
  im=get_image(im_int)
  gt_bboxes,dpm_bboxes,detected_dpm_bboxes=get_bbox_dict(im_int)
  return render_to_response('show_dpm/show_pic.html', {'image':im,'gt_bboxes':gt_bboxes,'dpm_bboxes':dpm_bboxes,'detected_dpm_bboxes':detected_dpm_bboxes})
 
def get_image(imageid):
  synsetid=145622
  db = connect_to_db('bbox_collection_gsv') 
  img_query='select myori_url, oriwidth,oriheight from imagenet_bbox.view_allimage where synsetid=%d and imageid=%d'%(synsetid, imageid) 
  cursor = db.cursor()
  cursor.execute(img_query)
  im=cursor.fetchone()
  db.close()
  im_dict={}
  im_dict['url']=im[0]
  im_dict['oriwidth']=im[1]
  im_dict['oriheight']=im[2]
  return im_dict
  
def visualize_boston(request):
  return render_to_response('show_dpm/visualize_boston.html')
