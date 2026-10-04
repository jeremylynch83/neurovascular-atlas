"""Angiogram-guided skull-base morphology; reference shapes, not measurements."""
def amend_skullbase(rows, relationships):
    byid={s['id']:s for s in rows}
    def a(key,t=1,side=None):return {'structure':'vein.'+key+('.'+side if side else ''),'fraction':t}
    def profile(width,depth,bones,centre,direction=None,support=.72,mode='nearest'):
        p=dict(kind='oval',width=width,depth=depth,centre=centre,bone_apposition=True,bone_names=bones,fit_mode=mode,wall_support=support,wall_clearance=.20,fair_mm=2)
        if direction is not None:p['bone_direction']=direction
        return p
    def path(points,radius,p=None):return {'points':points,'radius':radius,**({'profile':p} if p else {})}
    for s in rows:
        if s.get('profile',{}).get('bone_apposition'):s['profile']['wall_support']=.78
    for side,sign in [('right',1),('left',-1)]:
        def p(x,y,z):return [x if sign==1 else 1.3-x,y,z if sign==1 else z-.05]
        def update(key,**values):byid['vein.'+key+'.'+side].update(values)
        def at(key,t=1):return a(key,t,side)
        temporal='bone.temporal.'+side
        update('cavernous',points=[p(19,-51,49),p(17,-49,56),p(15,-47,63),p(14,-41,68),p(14,-35,69)],radius=[2.65,3.7,4.4,4.6,3.25],profile=dict(kind='oval',width=1.12,depth=.85,centre=[.65,-43,61],frame_normal=[sign,0,0]),additionalPaths=[path([at('cavernous',.2),p(20,-46,61),p(19,-39,67),at('cavernous',.98)],[2.2,2.7,2.3]),path([at('cavernous',.12),p(11,-47,58),p(10,-42,64),at('cavernous',.94)],[1.8,2.3,2.0])])
        update('sphenoparietal',points=[p(47,-28,84),p(38,-28,81),p(30,-29,77),p(22,-34,72),at('cavernous',.92)],radius=[.6,.8,1.05,1.2],profile=profile(1.35,.65,['bone.sphenoid'],[.65,-25,70],[0,.85,.5],mode='directional'))
        spheno=byid['vein.sphenoparietal.'+side]
        spheno['profile']['attachment_ramp_mm']=4
        spheno['description']=('This dural channel follows the lesser sphenoid wing and drains into the [cavernous sinus](#structure-vein.cavernous.'+side+'). It communicates with adjacent meningeal and diploic channels. Its relationship to the superficial Sylvian veins is variable and terminology differs between references. The represented [superficial middle cerebral vein](#structure-vein.superficial_middle_cerebral.'+side+') enters the cavernous region separately.')
        smcv=byid['vein.superficial_middle_cerebral.'+side]
        smcv['points']=smcv['points'][:3]+[p(49,-35,87),p(38,-36,80),p(26,-39,74),at('cavernous',.87)]
        smcv['parent']='vein.cavernous.'+side
        smcv['description']+=' In this selected drainage pattern it enters the cavernous region independently of the dural lesser-sphenoid-wing channel.'
        for r in relationships:
            if r['from']==smcv['id'] and r['to']==spheno['id'] and r['type']=='drains_to':r['to']='vein.cavernous.'+side
        update('superior_petrosal',points=[at('cavernous',.60),p(23,-59,60),p(35,-70,61),p(46,-81,63),at('sigmoid',0)],radius=[.95,1.15,1.25,1.4],profile=profile(1.25,.7,[temporal,'bone.sphenoid'],[.65,-73,78],[0,0,-1]))
        update('inferior_petrosal',points=[at('cavernous',.20),p(13,-58,54),p(16,-66,47),p(21,-72,40),p(27,-72,34),at('internal_jugular',.025)],radius=[1.05,1.25,1.3,1.4],profile=profile(1.35,.70,[temporal,'bone.occipital','bone.sphenoid'],[.65,-75,70],[0,.8,-.6]))
        byid['vein.transverse.'+side]['profile'].update(depth=.66,wall_support=.74)
        byid['vein.sigmoid.'+side]['profile'].update(depth=.76,wall_support=.76,fit_mode='nearest',bone_direction_mode='radial',bone_names=[temporal,'bone.occipital'],fit_until=.86)
        byid['vein.sigmoid.'+side]['continuation_length_mm']=14
        update('internal_jugular',radius=([2.4,4.25,4.65,4.4,4.5,4.8] if sign==1 else [2.4,3.75,4.1,3.9,4.0,4.2]))
        # Retain the established hypoglossal regional route; refine its calibre.
        update('anterior_condylar',radius=[.65,.9,1.35,1.1])
        update('lateral_condylar',radius=[.9,1.05,.8,.65])
        for target in ['inferior_petrosal','anterior_condylar']:
            r={'from':'vein.basilar_plexus','to':'vein.'+target+'.'+side,'type':'communicates_with'}
            if r not in relationships:relationships.append(r)
    clival=profile(1.35,.7,['bone.sphenoid','bone.occipital'],[.65,-78,66],[0,.85,-.53],support=.7)
    b=byid['vein.basilar_plexus']
    b.update(points=[[1.2,-51,62],[-.7,-55,56],[2,-60,49],[.2,-65,41],a('marginal',.5)],radius=[.58,.68,.55,.60,.52],profile=clival,additionalPaths=[
        path([a('cavernous',.2,'right'),[11,-54,57],[9.5,-58,53],[12,-62,48],[10,-67,40],a('anterior_condylar',0,'right')],[.65,.8,.6,.5],clival),
        path([a('cavernous',.22,'left'),[-8,-54,58],[-10,-59,52],[-7,-64,46],[-8,-68,39],a('anterior_condylar',0,'left')],[.7,.65,.75,.5],clival),
        path([a('inferior_petrosal',.22,'right'),[7,-53,59],[1.2,-54,58],[-6,-56,55],a('inferior_petrosal',.28,'left')],[.48,.65,.5],clival),
        path([[9.5,-58,53],[4,-58,52],[-1,-59,50],[-7,-61,48],[-7,-64,46]],[.6,.55,.7,.55],clival),
        path([a('inferior_petrosal',.57,'right'),[9,-64,45],[4,-63,47],[2,-60,49]],[.6,.7,.55],clival),
        path([[10,-67,40],[4,-65,42],[.2,-65,41],[-3,-67,40],[-8,-68,39]],[.55,.65,.48],clival),
        path([[10,-67,40],[6,-62,47],[1,-58,52],[-2,-55,56]],[.48,.56,.45],clival),
        path([[-7,-64,46],[-3,-62,48],[2,-60,49],[6,-56,55],[11,-54,57]],[.5,.6,.55],clival),
        path([a('inferior_petrosal',.62,'left'),[-8,-66,43],[-3,-67,40],a('marginal',.43)],[.55,.65,.5],clival),
        path([[10,-67,40],[6,-70,37],a('marginal',.58)],[.48,.6,.45],clival)])
    b['description']+=' It forms a variable plexiform network along the posterior clivus, with communications to both [inferior petrosal sinuses](#structure-vein.inferior_petrosal.right). The displayed interconnected channels represent one selected reference pattern.'
    marginal=profile(1.25,.7,['bone.occipital'],[.65,-86,31],support=.72)
    byid['vein.marginal'].update(radius=[.7,.85,.65,.9,.75,.7,.95,.8,.7],profile=marginal,additionalPaths=[path([a('marginal',.07),[15,-101,32],[21,-92,30],a('marginal',.3)],[.45,.6,.45],marginal),path([a('marginal',.64),[-18,-89,31],[-12,-101,31],a('marginal',.95)],[.48,.55,.45],marginal),path([a('marginal',.32),a('anterior_condylar',0,'right')],[.65,.8]),path([a('marginal',.67),a('anterior_condylar',0,'left')],[.6,.8])])
    byid['vein.anterior_intercavernous'].update(radius=[.8,1.0,.85],profile=dict(kind='oval',width=1.0,depth=.7,centre=[.65,-35,60],frame_normal=[0,0,1]))
    byid['vein.posterior_intercavernous'].update(points=[a('cavernous',.6,'right'),[6,-48,65],[.65,-49,65],[-5,-48,65],a('cavernous',.6,'left')],radius=[.75,1.1,.85],profile=profile(1.15,.7,['bone.sphenoid'],[.65,-56,67],[0,1,-.2]))
