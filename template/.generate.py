import os
import shutil
from igm.render import igm_script
from igm.env import user
from extras import project_dir

multi_seed_string = "import os\n\n" + "if __name__ == \"__main__\":\n  for s in placeholder:\n    os.popen('python3 -u main_seed{}.py'.format(s))"


@igm_script
def generate_experiment():
    for item in user.task_path:
        src, dst = item['src'], item['dst']
        dst_dir = os.path.dirname(dst)
        dst_dir = os.path.join(project_dir, dst_dir)
        os.makedirs(dst_dir)
        shutil.copy(src, dst)
        if user.seed != [0]:
            if len(user.seed) > 1:
                for s in user.seed:
                    dst_s = dst.split('.py')[0] + '_seed{}.py'.format(s)
                    shutil.copy(dst, dst_s)
                    os.popen("sed -i '' 's/seed=0/seed={}/' {}".format(s, dst_s))
                    os.popen("sed -i '' 's/seed0/seed{}/' {}".format(s, dst_s))
                with open(dst, 'w') as f:
                    f.write(multi_seed_string)
                os.popen("sed -i '' 's/placeholder/{}/' {}".format(user.seed, dst))
            else:
                os.popen("sed -i '' 's/seed=0/seed={}/' {}".format(user.seed[0], dst))
                os.popen("sed -i '' 's/seed0/seed{}/' {}".format(user.seed[0], dst))
