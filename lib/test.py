import numpy as np
import torch
import time
import os
import trimesh
import math
import argparse

from skimage.measure import marching_cubes

from mise import MISE

def sphere_sdf(x, radius=0.5):
    return torch.linalg.norm(x, axis=-1) - radius

def run_mise(sdf, resolution_0, depth, threshold, device):

    extractor = MISE(resolution_0, depth, threshold)

    p = extractor.query()
    n_iterations = 0
    max_iterations = 8

    while p.shape[0] != 0:

        print(f'n_iterations: {n_iterations}')
        print(f'number of extractor queries: {len(p)}')

        pointsf = (p / extractor.resolution) - 0.5
        pointsf = torch.FloatTensor(pointsf, device=device)

        v = sdf(pointsf).detach().numpy().astype(np.float64)
        extractor.update(p, v)
        p = extractor.query()
        n_iterations += 1
        if (n_iterations >= max_iterations):
            break
    return extractor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output-mesh',
        default=None,
        help='Output mesh path. If not provided, no output is saved.'
    )
    args = parser.parse_args()
    resolution_0 = 32 # Resolution in the first iteration
    depth = 4   # Number of subdivisions of the initial resolution. 
                # Final resolution = 2^(log2(resolution_0)*depth)
    threshold = 1e-5 # value of the occupancy that marks surface 

    print(
        f'Initial resolution: {resolution_0} \n'
        f'Number of subdivisions: {depth} \n'
        f'Final resolution: {2**(math.log2(resolution_0) + depth)}'
        )

    device = torch.device('cpu') # TODO: cuda_if_available

    t0 = time.time()
    extractor = run_mise(sphere_sdf, resolution_0, depth, threshold, device)
    print('Time to sparse values: %f' % (time.time() - t0))
    dense_values = extractor.to_dense()
    print('Time to dense values: %f' % (time.time() - t0))
    vertices, faces, normals, values = marching_cubes(volume=dense_values, level=0)
    print('Time to mesh: %f' % (time.time() - t0))

    if args.output_mesh:
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        mesh.export(args.output_mesh)

if __name__ == '__main__':
    main()